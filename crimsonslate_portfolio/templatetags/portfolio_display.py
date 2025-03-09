from typing import Any

from django.template import Library

from crimsonslate_portfolio.models import Media

register = Library()


@register.inclusion_tag("portfolio/media/display.html")
def media_display(
    media: Media,
    css_class: str | None = None,
    force_image: bool = False,
) -> dict[str, Any]:
    src = media.thumb.url if force_image and not media.is_image else media.source.url
    return {
        "title": media.title,
        "class": css_class,
        "image": force_image if force_image else media.is_image,
        "src": src,
        "link": media.get_absolute_url(),
    }
