from django.template import Library
from easy_thumbnails.files import get_thumbnailer

from crimsonslate_portfolio.models import Media

register = Library()


@register.inclusion_tag("portfolio/media/display.html")
def display_media(
    media: Media,
    css_class: str = "",
    force_image: bool = True,
) -> dict[str, str | bool]:
    src = media.source.url
    if force_image and not media.is_image:
        thumbnailer = get_thumbnailer(media.source)
        options = {"size": (100, 100), "crop": True}
        src = thumbnailer.get_thumbnail(options)
    return {
        "src": src,
        "class": css_class,
        "image": media.is_image or force_image,
        "alt": media.title,
    }
