from typing import Any

from django import forms
from django.db.models import QuerySet
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
    ListView,
)

from crimsonslate_portfolio.models import Media


class MediaDetailView(DetailView):
    content_type = "text/html"
    context_object_name = "media"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get"]
    model = Media
    partial_template_name = "portfolio/media/partials/_detail.html"
    template_name = "portfolio/media/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = self.get_object().title
        return context

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.htmx_request = bool(request.headers.get("HX-Request"))
        if self.htmx_request:
            self.template_name = self.partial_template_name

    def get_queryset(self) -> QuerySet:
        queryset = Media.objects.all()
        if not self.request.user or not self.request.user.is_staff:
            queryset = Media.objects.filter(is_hidden=False)
        return queryset


class MediaCreateView(CreateView):
    content_type = "text/html"
    context_object_name = "media"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Create"}
    fields = ["source", "thumb", "title", "subtitle", "desc", "is_hidden", "categories"]
    http_method_names = ["get", "post", "delete"]
    model = Media
    partial_template_name = "portfolio/media/partials/_create.html"
    success_url = reverse_lazy("portfolio gallery")
    template_name = "portfolio/media/create.html"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.htmx_request = bool(request.headers.get("HX-Request"))
        if self.htmx_request:
            self.template_name = self.partial_template_name

    def form_valid(self, form: forms.Form) -> HttpResponseRedirect:
        super().form_valid(form=form)
        media: Media = self.get_object()
        return HttpResponseRedirect(self.get_success_url(media))

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.htmx_request:
            return HttpResponse(status=403)
        return HttpResponse(b"", status=200)

    def get_success_url(self, media: Media | None = None) -> str:
        if media is not None:
            return reverse("media detail", kwargs={"slug": media.slug})
        return super().get_success_url()


class MediaDeleteView(DeleteView):
    content_type = "text/html"
    context_object_name = "media"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post", "delete"]
    model = Media
    partial_template_name = "portfolio/media/partials/_delete.html"
    success_url = reverse_lazy("portfolio gallery")
    template_name = "portfolio/media/delete.html"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_template_name

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = f"Delete {self.get_object().title}"
        return context

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.headers.get("HX-Request"):
            return HttpResponse(status=403)
        self.post(request, *args, **kwargs)
        return HttpResponse(b"", status=200)


class MediaUpdateView(UpdateView):
    content_type = "text/html"
    context_object_name = "media"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    model = Media
    fields = ["source", "thumb", "title", "subtitle", "desc", "is_hidden", "categories"]
    http_method_names = ["get", "post", "delete"]
    template_name = "portfolio/media/update.html"
    partial_template_name = "portfolio/media/partials/_update.html"
    success_url = reverse_lazy("portfolio gallery")

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.htmx_request = bool(request.headers.get("HX-Request"))
        if self.htmx_request:
            self.template_name = self.partial_template_name

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = f"Update {self.get_object().title}"
        return context

    def get_success_url(self, media: Media | None = None) -> str:
        if media is not None:
            return reverse("media detail", kwargs={"slug": media.slug})
        return super().get_success_url()

    def form_valid(self, form: forms.Form) -> HttpResponseRedirect:
        super().form_valid(form=form)
        return HttpResponseRedirect(self.get_success_url(self.object))

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponse(b"", status=200)


class MediaGalleryView(ListView):
    allow_empty = True
    content_type = "text/html"
    context_object_name = "medias"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Gallery"}
    http_method_names = ["get"]
    model = Media
    ordering = "-date_created"
    partial_template_name = "portfolio/media/_list.html"
    queryset = Media.objects.all()
    template_name = "portfolio/media/list.html"
    paginate_by = 12

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.htmx_request = bool(request.headers.get("HX-Request"))
        if self.htmx_request:
            self.template_name = self.partial_template_name

    def get_queryset(self) -> QuerySet:
        queryset = Media.objects.all()
        if not self.request.user or not self.request.user.is_staff:
            queryset = queryset.exclude(is_hidden=True)
        return queryset


class MediaSearchView(TemplateView):
    template_name = "portfolio/media/search.html"
    partial_template_name = "portfolio/media/partials/_search.html"
    content_type = "text/html"
    http_method_names = ["get"]
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_template_name


class MediaSearchResultsView(ListView):
    allow_empty = True
    content_type = "text/html"
    context_object_name = "search_results"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post", "delete"]
    model = Media
    ordering = "-title"
    queryset = Media.objects.exclude(is_hidden=True)
    template_name = "portfolio/media/search.html"
    partial_template_name = "portfolio/media/partials/_search.html"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_template_name
