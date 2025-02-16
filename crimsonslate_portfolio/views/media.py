from typing import Any

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView,
)

from crimsonslate_portfolio.models import Media
from crimsonslate_portfolio.views.base import HtmxTemplateView, PortfolioProfileMixin


class MediaUploadView(LoginRequiredMixin, PortfolioProfileMixin, HtmxTemplateView):
    content_type = "text/html"
    http_method_names = ["get"]
    extra_context = {"title": "Upload", "class": "bg-violet-100"}
    template_name = "portfolio/media/upload.html"
    partial_template_name = "portfolio/media/partials/_upload.html"
    login_url = reverse_lazy("login")
    raise_exception = True
    permission_denied_message = "Please login and try again."


class MediaUploadSuccessView(PortfolioProfileMixin, HtmxTemplateView):
    content_type = "text/html"
    http_method_names = ["get"]
    extra_context = {"title": "Success", "class": ""}
    template_name = "portfolio/media/upload_success.html"
    partial_template_name = "portfolio/media/partials/_upload_success.html"


class MediaDetailView(DetailView, HtmxTemplateView, PortfolioProfileMixin):
    content_type = "text/html"
    http_method_names = ["get"]
    model = Media
    partial_template_name = "portfolio/media/partials/_detail.html"
    queryset = Media.objects.all().exclude(is_hidden=True)
    template_name = "portfolio/media/detail.html"

    def get_queryset(self) -> QuerySet:
        if self.request.user and self.request.user.is_staff:
            return Media.objects.all()
        return self.queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)


class MediaCreateView(CreateView, HtmxTemplateView, PortfolioProfileMixin):
    content_type = "text/html"
    extra_context = {"title": "Create", "class": "flex flex-col gap-2 p-4"}
    fields = ["source", "thumb", "title", "subtitle", "desc", "is_hidden", "categories"]
    http_method_names = ["get", "post", "delete"]
    model = Media
    partial_template_name = "portfolio/media/partials/_create.html"
    template_name = "portfolio/media/create.html"
    success_url = reverse_lazy("upload success")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = None
        return super().get_context_data(**kwargs)


class MediaDeleteView(DeleteView, HtmxTemplateView, PortfolioProfileMixin):
    content_type = "text/html"
    http_method_names = ["get", "post", "delete"]
    model = Media
    partial_template_name = "portfolio/media/partials/_delete.html"
    success_url = reverse_lazy("gallery")
    template_name = "portfolio/media/delete.html"


class MediaUpdateView(UpdateView, HtmxTemplateView, PortfolioProfileMixin):
    content_type = "text/html"
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
            return reverse("detail media", kwargs={"slug": media.slug})
        return super().get_success_url()

    def form_valid(self, form: forms.Form) -> HttpResponseRedirect:
        super().form_valid(form=form)
        media: Media = self.get_object()
        return HttpResponseRedirect(self.get_success_url(media))


class MediaCarouselView(ListView, HtmxTemplateView, PortfolioProfileMixin):
    allow_empty = False
    content_type = "text/html"
    context_object_name = "carousel_item"
    http_method_names = ["get"]
    model = Media
    ordering = "date_created"
    paginate_by = 3
    partial_template_name = "portfolio/media/partials/_carousel.html"
    queryset = Media.objects.all().exclude(is_hidden=True)
    template_name = "portfolio/media/carousel.html"


class MediaGalleryView(ListView, HtmxTemplateView, PortfolioProfileMixin):
    allow_empty = True
    content_type = "text/html"
    extra_context = {"title": "Gallery"}
    http_method_names = ["get"]
    model = Media
    ordering = "date_created"
    paginate_by = 12
    partial_template_name = "portfolio/media/partials/_gallery.html"
    queryset = Media.objects.all().exclude(is_hidden=True)
    template_name = "portfolio/media/gallery.html"

    def get_queryset(self) -> QuerySet:
        if self.request.user and self.request.user.is_staff:
            return Media.objects.all()
        return self.queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object_list = self.get_queryset()
        return super().get_context_data(**kwargs)


class MediaSearchView(HtmxTemplateView, PortfolioProfileMixin):
    content_type = "text/html"
    http_method_names = ["get"]
    extra_context = {"title": "Search"}
    partial_template_name = "portfolio/media/partials/_search.html"
    template_name = "portfolio/media/search.html"


class MediaSearchResultsView(ListView, HtmxTemplateView, PortfolioProfileMixin):
    allow_empty = True
    content_type = "text/html"
    context_object_name = "search_results"
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
