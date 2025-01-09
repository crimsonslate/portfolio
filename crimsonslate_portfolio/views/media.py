from typing import Any

from django import forms
from django.db.models import QuerySet
from django.core.files import File
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
    ListView,
)

from crimsonslate_portfolio.models import Media, MediaSourceFile
from crimsonslate_portfolio.views.htmx import HtmxView


class MediaDetailView(DetailView, HtmxView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get"]
    model = Media
    partial_template_name = "portfolio/media/partials/_detail.html"
    queryset = Media.objects.all().exclude(is_hidden=True)
    template_name = "portfolio/media/detail.html"

    def get_queryset(self) -> QuerySet:
        if self.request.user and self.request.user.is_staff:
            return Media.objects.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = self.get_object().title
        return context


class MediaCreateView(LoginRequiredMixin, CreateView, HtmxView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Create"}
    fields = ["source", "thumb", "title", "subtitle", "desc", "is_hidden", "categories"]
    http_method_names = ["get", "post", "delete"]
    model = Media
    partial_template_name = "portfolio/media/partials/_create.html"
    success_url = reverse_lazy("gallery")
    template_name = "portfolio/media/create.html"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.file: File = MediaSourceFile.objects.get(pk=self.kwargs["pk"])

    def get_initial(self) -> dict[str, Any]:
        initial: dict[str, Any] = super().get_initial()
        initial["source"] = self.file
        return initial


class MediaDeleteView(LoginRequiredMixin, DeleteView, HtmxView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post", "delete"]
    model = Media
    partial_template_name = "portfolio/media/partials/_delete.html"
    success_url = reverse_lazy("gallery")
    template_name = "portfolio/media/delete.html"


class MediaUpdateView(LoginRequiredMixin, UpdateView, HtmxView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    fields = ["source", "thumb", "title", "subtitle", "desc", "is_hidden", "categories"]
    http_method_names = ["get", "post", "delete"]
    model = Media
    partial_template_name = "portfolio/media/partials/_update.html"
    queryset = Media.objects.all().exclude(is_hidden=True)
    success_url = reverse_lazy("gallery")
    template_name = "portfolio/media/update.html"

    def get_queryset(self) -> QuerySet:
        if self.request.user and self.request.user.is_staff:
            return Media.objects.all()
        return super().get_queryset()

    def get_success_url(self, media: Media | None = None) -> str:
        if media is not None:
            return reverse("media detail", kwargs={"slug": media.slug})
        return super().get_success_url()

    def form_valid(self, form: forms.Form) -> HttpResponseRedirect:
        super().form_valid(form=form)
        media: Media = self.get_object()
        return HttpResponseRedirect(self.get_success_url(media))


class MediaCarouselView(ListView, HtmxView):
    allow_empty = False
    content_type = "text/html"
    context_object_name = "carousel_item"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get"]
    model = Media
    ordering = "date_created"
    paginate_by = 1
    partial_template_name = "portfolio/media/partials/_carousel.html"
    queryset = Media.objects.all().exclude(is_hidden=True)
    template_name = "portfolio/media/carousel.html"


class MediaGalleryView(ListView, HtmxView):
    allow_empty = True
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Gallery"}
    http_method_names = ["get"]
    model = Media
    ordering = "date_created"
    paginate_by = 12
    partial_template_name = "portfolio/media/partials/_list.html"
    queryset = Media.objects.all().exclude(is_hidden=True)
    template_name = "portfolio/media/list.html"

    def get_queryset(self) -> QuerySet:
        if self.request.user and self.request.user.is_staff:
            return Media.objects.all()
        return super().get_queryset()


class MediaSearchView(TemplateView, HtmxView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get"]
    partial_template_name = "portfolio/media/partials/_search.html"
    template_name = "portfolio/media/search.html"


class MediaSearchResultsView(ListView, HtmxView):
    allow_empty = True
    content_type = "text/html"
    context_object_name = "search_results"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post", "delete"]
    model = Media
    ordering = "title"
    partial_template_name = "portfolio/media/partials/_search.html"
    queryset = Media.objects.all().exclude(is_hidden=True)
    template_name = "portfolio/media/search.html"

    def get_queryset(self) -> QuerySet:
        if self.request.user and self.request.user.is_staff:
            return Media.objects.all()
        return super().get_queryset()
