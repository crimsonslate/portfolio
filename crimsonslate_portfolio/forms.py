from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_image_file_extension
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.forms import widgets

from crimsonslate_portfolio.validators import validate_media_file_extension


class PortfolioAuthenticationForm(AuthenticationForm):
    """A basic authentication form."""


class MediaEditForm(forms.Form):
    base_attrs: dict[str, Any] = {
        "class": "w-full block bg-white rounded-md p-4 mt-2 mb-4 dark:text-gray-50 dark:bg-gray-800"
    }

    source = forms.FileField(
        label=_("Source"),
        help_text=_("Upload a video or an image."),
        widget=widgets.FileInput(attrs=base_attrs),
        allow_empty_file=False,
        validators=[validate_media_file_extension],
    )
    thumb = forms.FileField(
        label=_("Thumbnail"),
        help_text=_("Upload an optional thumbnail."),
        widget=widgets.ClearableFileInput(attrs=base_attrs),
        allow_empty_file=False,
        validators=[validate_image_file_extension],
    )
    title = forms.CharField(
        label=_("Title"),
        widget=widgets.TextInput(attrs=base_attrs),
    )
    subtitle = forms.CharField(
        label=_("Subtitle"),
        widget=widgets.TextInput(attrs=base_attrs),
    )
    desc = forms.CharField(
        label=_("Description"),
        widget=widgets.Textarea(attrs=base_attrs),
    )
    is_hidden = forms.FileField(
        label=_("Set as hidden?"),
        widget=widgets.CheckboxInput(attrs=base_attrs),
    )


class MediaUploadForm(forms.Form):
    base_attrs: dict[str, Any] = {
        "class": "w-full block bg-white rounded-md p-4 mt-2 mb-4 dark:text-gray-50 dark:bg-gray-800"
    }

    source = forms.FileField(
        label=_("Source"),
        help_text=_("Upload a video or an image."),
        widget=widgets.FileInput(attrs=base_attrs),
        allow_empty_file=False,
        validators=[validate_media_file_extension],
    )
    thumb = forms.FileField(
        label=_("Thumbnail"),
        help_text=_("Upload an optional thumbnail."),
        widget=widgets.FileInput(attrs=base_attrs),
        allow_empty_file=False,
        validators=[validate_image_file_extension],
        required=False,
    )
    title = forms.CharField(
        label=_("Title"),
        widget=widgets.TextInput(attrs=base_attrs),
        max_length=64,
    )
    subtitle = forms.CharField(
        label=_("Subtitle"),
        widget=widgets.TextInput(attrs=base_attrs),
        required=False,
    )
    desc = forms.CharField(
        label=_("Description"),
        widget=widgets.Textarea(attrs=base_attrs),
        required=False,
    )
    is_hidden = forms.FileField(
        label=_("Set as hidden?"),
        help_text=_(
            """If you're not ready to share this media with the world,
            or if you'd rather just store it here, check this box."""
        ),
        widget=widgets.CheckboxInput(attrs={"class": "accent-blue-700"}),
        required=False,
    )


class MediaSearchForm(forms.Form):
    base_attrs: dict[str, Any] = {
        "class": "w-full block bg-white rounded-md p-4 mt-2 mb-4 dark:text-gray-50 dark:bg-gray-800"
    }

    search = forms.CharField(
        max_length=64,
        widget=widgets.Input(
            attrs={
                "id": "id-search",
                "name": "search",
                "type": "search",
                "class": base_attrs["class"],
                "hx-post": reverse_lazy("portfolio search"),
                "hx-trigger": "input changed delay:150ms, search",
                "hx-target": "#id-search-results",
                "hx-indicator": ".htmx-indicator",
                "hx-swap": "outerHTML",
                "required": False,
                "placeholder": "Search...",
            },
        ),
    )
