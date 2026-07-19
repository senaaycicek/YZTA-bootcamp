"""Designer Agent: ürün bilgisinden görsel üretim promptu oluşturur."""


def generate_image_prompt(product: dict) -> str:
    """Ürün özelliklerinden İngilizce, detaylı bir görsel üretim promptu üretir.

    product: materyal, tarz, renk, kategori, kullanim_amaci, hedef_kitle
    """
    material = product["materyal"]
    style = product["tarz"]
    color = product["renk"]
    category = product["kategori"]
    use_case = product["kullanim_amaci"]
    audience = product["hedef_kitle"]

    return (
        f"A professional e-commerce product photo of a {color} {material} {category}, "
        f"designed in a {style} style for {audience}. "
        f"The product should be shown in a clean studio setup with softbox lighting, "
        f"subtle shadows, a premium minimal background, balanced composition, and a natural camera angle. "
        f"The overall mood should reflect {use_case}, with crisp textures, realistic materials, sharp focus, "
        f"high dynamic range, ultra detailed, 8k, professional product photography."
    )
