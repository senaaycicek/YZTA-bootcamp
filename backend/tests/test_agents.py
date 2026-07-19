"""designer_agent, copywriter_agent ve image_adapter birim testleri."""
from base64 import b64encode
import json

import pytest

from app.agents import copywriter_agent, designer_agent, image_adapter
from app.agents.llm_client import LLMError

PRODUCT = {
    "materyal": "seramik",
    "tarz": "minimalist",
    "renk": "mat siyah",
    "kategori": "kahve kupası",
    "kullanim_amaci": "günlük kahve keyfi",
    "hedef_kitle": "genç profesyoneller",
}


def test_designer_agent_returns_prompt(monkeypatch):
    prompt = designer_agent.generate_image_prompt(PRODUCT)

    assert prompt.startswith("A professional e-commerce product photo of a mat siyah seramik kahve kupası")
    assert "minimalist style" in prompt
    assert "genç profesyoneller" in prompt
    assert "softbox lighting" in prompt
    assert prompt.endswith("professional product photography.")


def test_copywriter_agent_parses_json(monkeypatch):
    response = {
        "baslik": "Minimalist Mat Siyah Seramik Kupa",
        "aciklama": "Harika bir kupa. " * 30,
        "anahtar_kelimeler": ["kupa", "seramik", "siyah kupa", "kahve", "minimalist"],
    }
    monkeypatch.setattr(
        copywriter_agent.llm_client, "chat", lambda *a, **k: json.dumps(response)
    )

    result = copywriter_agent.generate_marketing_copy(PRODUCT, "image prompt")

    assert result["baslik"] == response["baslik"]
    assert len(result["anahtar_kelimeler"]) == 5


def test_copywriter_agent_strips_code_fences(monkeypatch):
    raw = '```json\n{"baslik": "B", "aciklama": "A", "anahtar_kelimeler": ["k1"]}\n```'
    monkeypatch.setattr(copywriter_agent.llm_client, "chat", lambda *a, **k: raw)

    result = copywriter_agent.generate_marketing_copy(PRODUCT, "prompt")

    assert result["baslik"] == "B"


def test_copywriter_agent_invalid_json_raises(monkeypatch):
    monkeypatch.setattr(
        copywriter_agent.llm_client, "chat", lambda *a, **k: "bu json değil"
    )

    with pytest.raises(LLMError):
        copywriter_agent.generate_marketing_copy(PRODUCT, "prompt")


def test_copywriter_agent_missing_field_raises(monkeypatch):
    monkeypatch.setattr(
        copywriter_agent.llm_client, "chat", lambda *a, **k: '{"baslik": "B"}'
    )

    with pytest.raises(LLMError):
        copywriter_agent.generate_marketing_copy(PRODUCT, "prompt")


def test_openai_image_generator_decodes_b64_payload(monkeypatch):
    encoded = b64encode(image_adapter.PLACEHOLDER_PNG).decode("ascii")

    class FakeImageData:
        b64_json = encoded
        url = None

    class FakeResponse:
        data = [FakeImageData()]

    class FakeClient:
        class images:
            @staticmethod
            def generate(**kwargs):
                return FakeResponse()

    monkeypatch.setattr(image_adapter, "_get_openai_client", lambda: FakeClient())

    result = image_adapter.OpenAIImageGenerator().generate("prompt")

    assert result == image_adapter.PLACEHOLDER_PNG


def test_openai_image_generator_downloads_url_payload(monkeypatch):
    class FakeImageData:
        b64_json = None
        url = "https://example.com/generated.png"

    class FakeResponse:
        data = [FakeImageData()]

    class FakeClient:
        class images:
            @staticmethod
            def generate(**kwargs):
                return FakeResponse()

    class FakeDownloadResponse:
        content = b"downloaded-image-bytes"

        def raise_for_status(self):
            return None

    monkeypatch.setattr(image_adapter, "_get_openai_client", lambda: FakeClient())
    monkeypatch.setattr(image_adapter.httpx, "get", lambda url, timeout: FakeDownloadResponse())

    result = image_adapter.OpenAIImageGenerator().generate("prompt")

    assert result == b"downloaded-image-bytes"


def test_get_image_generator_prefers_openai_when_key_exists(monkeypatch):
    monkeypatch.setattr(image_adapter.settings, "OPENAI_API_KEY", "test-key")

    generator = image_adapter.get_image_generator()

    assert isinstance(generator, image_adapter.OpenAIImageGenerator)
