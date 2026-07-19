"""Ürün iş mantığı — route katmanından ayrı tutulur."""
from pathlib import Path

from sqlalchemy.orm import Session

from ..agents.image_adapter import PLACEHOLDER_PNG, get_image_generator
from ..models import Product
from ..schemas import ProductCreate
from . import orchestrator

_GENERATED_IMAGES_DIR = Path(__file__).resolve().parents[2] / "generated_images"


def _image_path(product_id: int) -> Path:
    return _GENERATED_IMAGES_DIR / f"product_{product_id}.png"


def ensure_product_image(product: Product, force: bool = False) -> Path:
    prompt = product.uretilen_gorsel_prompt
    if not prompt:
        raise ValueError("Bu ürün için görsel prompt henüz üretilmedi.")

    image_path = _image_path(product.id)
    if image_path.exists() and not force:
        if image_path.read_bytes() != PLACEHOLDER_PNG:
            return image_path

    _GENERATED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    image_bytes = get_image_generator().generate(prompt)
    image_path.write_bytes(image_bytes)
    return image_path


def create_product(db: Session, user_id: int, payload: ProductCreate) -> Product:
    product = Product(user_id=user_id, **payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, user_id: int, product_id: int) -> Product | None:
    return (
        db.query(Product)
        .filter(Product.id == product_id, Product.user_id == user_id)
        .first()
    )


def list_products(db: Session, user_id: int) -> list[Product]:
    return (
        db.query(Product)
        .filter(Product.user_id == user_id)
        .order_by(Product.olusturulma_tarihi.desc())
        .all()
    )


def generate_for_product(db: Session, product: Product) -> dict:
    """Orchestrator'ı çalıştırır ve sonucu ürüne kaydeder."""
    product_info = {
        "materyal": product.materyal,
        "tarz": product.tarz,
        "renk": product.renk,
        "kategori": product.kategori,
        "kullanim_amaci": product.kullanim_amaci,
        "hedef_kitle": product.hedef_kitle,
    }
    result = orchestrator.run_pipeline(product_info)

    product.uretilen_gorsel_prompt = result["gorsel_prompt"]
    product.uretilen_baslik = result["baslik"]
    product.uretilen_aciklama = result["aciklama"]
    product.uretilen_anahtar_kelimeler = ", ".join(result["anahtar_kelimeler"])
    db.commit()
    db.refresh(product)
    ensure_product_image(product, force=True)

    return result
