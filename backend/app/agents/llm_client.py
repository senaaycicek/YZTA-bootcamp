"""OpenAI çağrıları için ortak istemci katmanı.

Tüm agent'lar LLM'e buradan erişir; böylece model/sağlayıcı değişikliği
tek noktadan yapılır ve testlerde kolayca mock'lanır.
"""
import json
import re

from openai import OpenAI, OpenAIError

from ..config import settings


class LLMError(Exception):
    """LLM çağrısı başarısız olduğunda fırlatılır; route katmanı bunu
    kullanıcı dostu bir HTTP hatasına çevirir."""


_client: OpenAI | None = None


def _fallback_enabled() -> bool:
    return settings.LLM_FALLBACK_ENABLED


def _extract_value(text: str, labels: tuple[str, ...]) -> str:
    for label in labels:
        match = re.search(rf"{re.escape(label)}\s*:\s*(.+)", text)
        if match:
            return match.group(1).strip()
    return ""


def _mock_designer_response(user_prompt: str) -> str:
    material = _extract_value(user_prompt, ("Material", "Materyal"))
    style = _extract_value(user_prompt, ("Style", "Tarz"))
    color = _extract_value(user_prompt, ("Color", "Renk"))
    category = _extract_value(user_prompt, ("Category", "Kategori"))
    use_case = _extract_value(user_prompt, ("Intended use", "Kullanım amacı", "Kullanim amaci"))
    audience = _extract_value(user_prompt, ("Target audience", "Hedef kitle"))

    details = ", ".join(
        value for value in (material, style, color, category, use_case, audience) if value
    )
    prompt = (
        f"A professional e-commerce product photo of a {details or 'stylish product'}, "
        "shot in a clean studio with softbox lighting, subtle shadows, premium styling, "
        "balanced composition, sharp focus, high dynamic range, ultra detailed, 8k"
    )
    return prompt


def _mock_copywriter_response(user_prompt: str) -> str:
    material = _extract_value(user_prompt, ("- Materyal:", "Materyal"))
    style = _extract_value(user_prompt, ("- Tarz:", "Tarz"))
    color = _extract_value(user_prompt, ("- Renk:", "Renk"))
    category = _extract_value(user_prompt, ("- Kategori:", "Kategori"))
    use_case = _extract_value(user_prompt, ("- Kullanım amacı:", "Kullanım amacı", "Kullanim amaci", "- Kullanım amacI:"))
    audience = _extract_value(user_prompt, ("- Hedef kitle:", "Hedef kitle"))

    baslik_parts = [part for part in (style, color, material, category) if part]
    baslik = " ".join(baslik_parts)[:70] or "Premium Ürün"
    aciklama = (
        f"{baslik}, günlük kullanımdan hediye seçeneğine kadar geniş bir kullanım alanı sunar. "
        f"{material or 'Kaliteli'} yapısı, {style or 'özenli'} tasarımı ve {color or 'dikkat çekici'} görünümüyle "
        f"{audience or 'hedef kitleniz'} için güçlü bir satın alma motivasyonu oluşturur. "
        f"{category or 'Ürün'} kategorisinde öne çıkan bu seçenek, {use_case or 'günlük ihtiyaçlar'} için "
        "hem estetik hem de işlevsel bir deneyim sağlar. SEO uyumlu, sade ve satış odaklı anlatımıyla "
        "ürün sayfalarında güven oluşturmak ve dönüşümü artırmak için hazırlanmıştır."
    )
    anahtar_kelimeler = [
        keyword
        for keyword in [
            category or "ürün",
            material or "kaliteli ürün",
            style or "modern tasarım",
            color or "şık görünüm",
            use_case or "günlük kullanım",
        ]
        if keyword
    ][:5]

    return json.dumps(
        {
            "baslik": baslik,
            "aciklama": aciklama,
            "anahtar_kelimeler": anahtar_kelimeler,
        },
        ensure_ascii=False,
    )


def _mock_chat(system_prompt: str, user_prompt: str) -> str:
    if "JSON formatında" in system_prompt or "baslik" in system_prompt:
        return _mock_copywriter_response(user_prompt)
    return _mock_designer_response(user_prompt)


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise LLMError(
                "OPENAI_API_KEY tanımlı değil. Lütfen ortam değişkenini ayarlayın."
            )
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def chat(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """Tek turluk bir chat.completions çağrısı yapar ve metni döndürür."""
    try:
        response = _get_client().chat.completions.create(
            model=settings.OPENAI_MODEL,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            raise LLMError("LLM boş yanıt döndürdü.")
        return content.strip()
    except OpenAIError as exc:
        if _fallback_enabled():
            return _mock_chat(system_prompt, user_prompt)
        raise LLMError(f"LLM çağrısı başarısız oldu: {exc}") from exc
    except LLMError:
        if _fallback_enabled():
            return _mock_chat(system_prompt, user_prompt)
        raise
