from django.forms import ModelForm
from django.urls import reverse

from crimsonslate_portfolio.models import Media


class MediaUploadForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "source",
            "thumb",
            "title",
            "subtitle",
            "desc",
            "is_hidden",
            "categories",
        ]


class MediaEditForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "source",
            "thumb",
            "title",
            "subtitle",
            "desc",
            "is_hidden",
            "categories",
            "date_created",
        ]


class MediaSearchForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "title",
            "categories",
            "date_created",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["title"].attrs.update(
            {
                "hx-post": reverse("portfolio search"),
                "hx-target": "#id-search-results",
                "hx-swap": "outerHTML",
                "hx-trigger": "search, keyup changed delay:150ms",
                "hx-indicator": ".htmx-indicator",
            }
        )
