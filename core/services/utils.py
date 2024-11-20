from uuid import uuid4
from unidecode import unidecode
from django.utils.text import slugify


def unique_slugify(instance, name: str):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(unidecode(name))

    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{unique_slug}-{uuid4().hex[:12]}"

    return unique_slug
