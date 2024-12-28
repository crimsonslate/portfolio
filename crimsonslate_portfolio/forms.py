from django import forms
from django.forms import ModelForm, widgets
from django.urls import reverse_lazy

from crimsonslate_portfolio.models import Media


class MediaUploadForm(forms.Form):
    file = forms.FileField()
    chunk_size = forms.IntegerField(
        min_value=64 * 2**10, max_value=256 * 2**10, step_size=64 + 2**10
    )
    upload_id = forms.CharField(widget=widgets.HiddenInput())
    part_id = forms.IntegerField(
        min_value=1, max_value=10000, widget=widgets.HiddenInput()
    )


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


class MediaSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        widget=widgets.TextInput(
            attrs={
                "hx-trigger": "load, keyup changed delay:150ms",
                "hx-post": reverse_lazy("portfolio search"),
                "class": "w-full block rounded p-2 border-gray-600",
                "autofocus": True,
                "autocomplete": False,
            }
        ),
    )

    def clean_title(self) -> str:
        if not self.cleaned_data.get("title"):
            self.cleaned_data["title"] = "*"
        return self.cleaned_data["title"]
