from django import template

register = template.Library()


PRODUCT_VECTOR_MAP = {
    "cards": "img/products/cards.svg",
    "dice": "img/products/dice.svg",
    "organizer": "img/products/organizer.svg",
    "tokens": "img/products/tokens.svg",
    "mat": "img/products/mat.svg",
    "default": "img/products/accessory.svg",
}


def _product_text(product):
    category = getattr(product, "category", None)
    parts = [
        getattr(product, "name", ""),
        getattr(category, "name", ""),
    ]
    return " ".join(parts).lower()


@register.filter
def product_vector(product):
    text = _product_text(product)

    if any(word in text for word in ("sleeve", "card", "кар", "протектор", "протек", "чех", "рукав")):
        return PRODUCT_VECTOR_MAP["cards"]
    if any(word in text for word in ("dice", "die", "куб", "дайс", "d20", "d6")):
        return PRODUCT_VECTOR_MAP["dice"]
    if any(word in text for word in ("organizer", "insert", "box", "органайзер", "встав", "короб")):
        return PRODUCT_VECTOR_MAP["organizer"]
    if any(word in text for word in ("token", "coin", "marker", "жетон", "маркер", "монет")):
        return PRODUCT_VECTOR_MAP["tokens"]
    if any(word in text for word in ("mat", "playmat", "ковр", "поле", "плеймат")):
        return PRODUCT_VECTOR_MAP["mat"]
    return PRODUCT_VECTOR_MAP["default"]
