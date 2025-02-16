from datetime import date

from django.core.files.storage import storages
from django.core.validators import (
    get_available_image_extensions,
    validate_image_file_extension,
)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from crimsonslate_portfolio.validators import validate_media_file_extension


class MediaCategory(models.Model):
    name = models.CharField(max_length=64)
    cover = models.ImageField(
        verbose_name="cover image",
        storage=storages["bucket"],
        upload_to="category/",
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return str(self.name)


class Media(models.Model):
    title = models.CharField(
        max_length=64,
        unique=True,
    )
    source = models.FileField(
        storage=storages["bucket"],
        upload_to="source/",
        validators=[validate_media_file_extension],
    )
    thumb = models.ImageField(
        blank=True,
        default=None,
        null=True,
        storage=storages["bucket"],
        upload_to="thumb/",
        validators=[validate_image_file_extension],
        verbose_name="thumbnail",
    )
    subtitle = models.CharField(max_length=128, blank=True, null=True, default=None)
    desc = models.TextField(
        verbose_name="description", max_length=2048, blank=True, null=True, default=None
    )
    slug = models.SlugField(
        max_length=64, unique=True, blank=True, null=True, default=None
    )
    is_hidden = models.BooleanField(default=False)
    is_image = models.BooleanField(blank=True, null=True, editable=False)
    categories = models.ManyToManyField("MediaCategory", default=None, blank=True)

    date_created = models.DateField(default=date.today)
    datetime_published = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["date_created"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "slug"],
                name="%(app_label)s_%(class)s_unique_title_and_slug",
            )
        ]

    def __str__(self) -> str:
        return str(self.title)

    def save(self, **kwargs) -> None:
        if self.is_image is None:
            self.is_image = self.file_extension in get_available_image_extensions()
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        return super().save(**kwargs)

    def get_absolute_url(self) -> str:
        return reverse("detail media", kwargs={"slug": self.slug})

    @property
    def file_extension(self) -> str | None:
        return self.source.file.name.split(".")[-1] if self.source else None
