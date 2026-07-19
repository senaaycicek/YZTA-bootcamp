"""API entegrasyon testleri: auth akışı ve ürün endpoint'leri."""

from pathlib import Path

from app.agents.image_adapter import ImageGenerationError
from app.agents import llm_client
from app.services import product_service
from app.services import orchestrator
from tests.conftest import SAMPLE_PRODUCT


# ---------- Auth ----------
def test_register_and_login(client):
    res = client.post(
        "/api/auth/register", json={"email": "a@b.com", "password": "sifre123"}
    )
    assert res.status_code == 201
    assert "access_token" in res.json()

    res = client.post(
        "/api/auth/login", json={"email": "a@b.com", "password": "sifre123"}
    )
    assert res.status_code == 200


def test_register_duplicate_email(client):
    client.post("/api/auth/register", json={"email": "a@b.com", "password": "sifre123"})
    res = client.post(
        "/api/auth/register", json={"email": "a@b.com", "password": "sifre456"}
    )
    assert res.status_code == 409


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={"email": "a@b.com", "password": "sifre123"})
    res = client.post("/api/auth/login", json={"email": "a@b.com", "password": "yanlis"})
    assert res.status_code == 401


def test_protected_route_requires_token(client):
    assert client.get("/api/products").status_code == 401
    assert client.get("/api/products", headers={"Authorization": "Bearer bozuk"}).status_code == 401


# ---------- Products ----------
def test_create_and_get_product(client, auth_headers):
    res = client.post("/api/products", json=SAMPLE_PRODUCT, headers=auth_headers)
    assert res.status_code == 201
    product_id = res.json()["id"]

    res = client.get(f"/api/products/{product_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["materyal"] == "seramik"

    res = client.get("/api/products", headers=auth_headers)
    assert len(res.json()) == 1


def test_user_cannot_see_others_products(client, auth_headers):
    res = client.post("/api/products", json=SAMPLE_PRODUCT, headers=auth_headers)
    product_id = res.json()["id"]

    res = client.post(
        "/api/auth/register", json={"email": "digeri@b.com", "password": "sifre123"}
    )
    other_headers = {"Authorization": f"Bearer {res.json()['access_token']}"}

    assert client.get(f"/api/products/{product_id}", headers=other_headers).status_code == 404
    assert client.get("/api/products", headers=other_headers).json() == []


def test_generate_saves_results(client, auth_headers, monkeypatch):
    fake_result = {
        "gorsel_prompt": "a beautiful mug prompt",
        "baslik": "Şık Seramik Kupa",
        "aciklama": "Uzun açıklama",
        "anahtar_kelimeler": ["kupa", "seramik", "kahve", "hediye", "minimalist"],
    }
    fake_image_bytes = b"fake-png-bytes"

    class FakeImageGenerator:
        def generate(self, prompt):
            return fake_image_bytes

    monkeypatch.setattr(orchestrator, "run_pipeline", lambda product: fake_result)
    monkeypatch.setattr(product_service, "get_image_generator", lambda: FakeImageGenerator())

    generated_images_dir = Path(product_service.__file__).resolve().parents[2] / "generated_images"
    monkeypatch.setattr(product_service, "_GENERATED_IMAGES_DIR", generated_images_dir)

    res = client.post("/api/products", json=SAMPLE_PRODUCT, headers=auth_headers)
    product_id = res.json()["id"]

    res = client.post(f"/api/products/{product_id}/generate", headers=auth_headers)
    assert res.status_code == 200
    body = res.json()
    assert body["gorsel_prompt"] == fake_result["gorsel_prompt"]
    assert body["product"]["uretilen_baslik"] == "Şık Seramik Kupa"

    image_path = generated_images_dir / f"product_{product_id}.png"
    assert image_path.exists()
    assert image_path.read_bytes() == fake_image_bytes

    res = client.get(f"/api/products/{product_id}/image", headers=auth_headers)
    assert res.status_code == 200
    assert res.headers["content-type"] == "image/png"
    assert res.content == fake_image_bytes

    # Sonuçlar kalıcı olarak kaydedilmiş olmalı
    res = client.get(f"/api/products/{product_id}", headers=auth_headers)
    assert res.json()["uretilen_anahtar_kelimeler"].startswith("kupa,")


def test_generate_llm_failure_returns_502(client, auth_headers, monkeypatch):
    from app.agents.llm_client import LLMError

    def failing_pipeline(product):
        raise LLMError("OPENAI_API_KEY tanımlı değil.")

    monkeypatch.setattr(orchestrator, "run_pipeline", failing_pipeline)

    res = client.post("/api/products", json=SAMPLE_PRODUCT, headers=auth_headers)
    product_id = res.json()["id"]

    res = client.post(f"/api/products/{product_id}/generate", headers=auth_headers)
    assert res.status_code == 502
    assert "İçerik üretimi başarısız" in res.json()["detail"]


def test_generate_uses_fallback_copy_when_openai_unavailable(
    client, auth_headers, monkeypatch
):
    monkeypatch.setattr(llm_client.settings, "OPENAI_API_KEY", "")
    monkeypatch.setattr(llm_client.settings, "LLM_FALLBACK_ENABLED", True)
    monkeypatch.setattr(llm_client, "_client", None)

    res = client.post("/api/products", json=SAMPLE_PRODUCT, headers=auth_headers)
    product_id = res.json()["id"]

    res = client.post(f"/api/products/{product_id}/generate", headers=auth_headers)
    assert res.status_code == 502
    assert "Görsel üretimi başarısız" in res.json()["detail"]


def test_product_image_returns_502_when_image_generation_fails(
    client, auth_headers, monkeypatch, tmp_path
):
    fake_result = {
        "gorsel_prompt": "a broken prompt",
        "baslik": "Başlık",
        "aciklama": "Açıklama",
        "anahtar_kelimeler": ["kupa", "seramik", "kahve", "hediye", "minimalist"],
    }

    def failing_generate(prompt):
        raise ImageGenerationError("Görsel üretilemedi.")

    class FailingImageGenerator:
        def generate(self, prompt):
            return failing_generate(prompt)

    monkeypatch.setattr(orchestrator, "run_pipeline", lambda product: fake_result)
    monkeypatch.setattr(product_service, "get_image_generator", lambda: FailingImageGenerator())

    generated_images_dir = tmp_path / "generated_images"
    monkeypatch.setattr(product_service, "_GENERATED_IMAGES_DIR", generated_images_dir)

    res = client.post("/api/products", json=SAMPLE_PRODUCT, headers=auth_headers)
    product_id = res.json()["id"]

    res = client.post(f"/api/products/{product_id}/generate", headers=auth_headers)
    assert res.status_code == 502
    assert "Görsel üretimi başarısız" in res.json()["detail"]

    image_path = generated_images_dir / f"product_{product_id}.png"
    assert not image_path.exists()
