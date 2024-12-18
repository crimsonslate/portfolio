from typing import Any
from django.forms import ModelForm, widgets

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
        widgets = {"title": widgets.Input({"type": "search"})}

    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()
        if not cleaned_data.get("title"):
            cleaned_data["title"] = "*"
        return cleaned_data
