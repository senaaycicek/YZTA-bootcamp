"""Görsel üretim API'leri için adapter katmanı.

OpenAI görsel üretimini normal akış olarak kullanır; test ve anahtarsız
çalışma senaryoları için yerel placeholder üretici içerir.
"""
from abc import ABC, abstractmethod
from base64 import b64decode

import httpx

from openai import OpenAI, OpenAIError

from ..config import settings

PLACEHOLDER_PNG = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j6ioAAAAASUVORK5CYII="
)


class ImageGeneratorAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> bytes:
        """Verilen prompt'tan bir görsel üretir ve ham PNG/JPG byte'larını döndürür."""


class ImageGenerationError(Exception):
    """Görsel üretimi başarısız olduğunda fırlatılır."""


class MockImageGenerator(ImageGeneratorAdapter):
    """Testler için deterministik görsel byte'ları üretir."""

    def generate(self, prompt: str) -> bytes:
        return PLACEHOLDER_PNG


_openai_client: OpenAI | None = None


def _get_openai_client() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        if not settings.OPENAI_API_KEY:
            raise ImageGenerationError("OPENAI_API_KEY tanımlı değil.")
        _openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _openai_client


def _download_image_bytes(image_url: str) -> bytes:
    response = httpx.get(image_url, timeout=30.0)
    response.raise_for_status()
    return response.content


class OpenAIImageGenerator(ImageGeneratorAdapter):
    """OpenAI image API ile görsel üretir."""

    def generate(self, prompt: str) -> bytes:
        try:
            response = _get_openai_client().images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024",
            )

            if not response.data:
                raise ImageGenerationError("OpenAI boş yanıt döndürdü.")

            image_data = response.data[0]
            encoded_image = getattr(image_data, "b64_json", None)
            if encoded_image:
                return b64decode(encoded_image)

            image_url = getattr(image_data, "url", None)
            if image_url:
                return _download_image_bytes(image_url)

            raise ImageGenerationError(
                "OpenAI görsel yanıtı beklenen formatta değil."
            )

        except OpenAIError as exc:
            raise ImageGenerationError(f"OpenAI görsel üretimi başarısız oldu: {exc}") from exc
        except httpx.HTTPError as exc:
            raise ImageGenerationError(f"OpenAI görseli indirilemedi: {exc}") from exc


def get_image_generator() -> ImageGeneratorAdapter:
    if settings.OPENAI_API_KEY:
        return OpenAIImageGenerator()
    raise ImageGenerationError("OPENAI_API_KEY tanımlı değil. Görsel üretimi için anahtar gerekli.")
