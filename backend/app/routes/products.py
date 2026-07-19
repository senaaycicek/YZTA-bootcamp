"""Ürün endpoint'leri — tümü JWT ile korunur."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..agents.image_adapter import ImageGenerationError
from ..agents.llm_client import LLMError
from ..auth.dependencies import get_current_user
from ..database import get_db
from ..models import User
from ..schemas import GenerateResult, ProductCreate, ProductOut
from ..services import product_service

router = APIRouter(prefix="/api/products", tags=["products"])


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return product_service.create_product(db, current_user.id, payload)


@router.get("", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return product_service.list_products(db, current_user.id)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = product_service.get_product(db, current_user.id, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
    return product


@router.post("/{product_id}/generate", response_model=GenerateResult)
def generate(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = product_service.get_product(db, current_user.id, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")

    try:
        result = product_service.generate_for_product(db, product)
    except LLMError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"İçerik üretimi başarısız oldu: {exc}",
        ) from exc
    except ImageGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Görsel üretimi başarısız oldu: {exc}",
        ) from exc

    return GenerateResult(
        product=ProductOut.model_validate(product),
        gorsel_prompt=result["gorsel_prompt"],
        baslik=result["baslik"],
        aciklama=result["aciklama"],
        anahtar_kelimeler=result["anahtar_kelimeler"],
    )


@router.get("/{product_id}/image")
def product_image(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = product_service.get_product(db, current_user.id, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")

    try:
        image_path = product_service.ensure_product_image(product)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ImageGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Görsel üretimi başarısız oldu: {exc}",
        ) from exc

    return FileResponse(image_path, media_type="image/png")
