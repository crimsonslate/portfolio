from typing import Any
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from crimsonslate_portfolio.models import MediaSourceFile
from crimsonslate_portfolio.views.base import HtmxView, PortfolioProfileMixin


class SourceFileDetailView(
    DetailView, HtmxView, PortfolioProfileMixin, LoginRequiredMixin
):
    content_type = "text/html"
    context_object_name = "file"
    extra_context = {"title": "File"}
    http_method_names = ["get"]
    login_url = reverse_lazy("login")
    model = MediaSourceFile
    partial_template_name = "portfolio/files/partials/_detail.html"
    permission_denied_message = "Please login and try again."
    queryset = MediaSourceFile.objects.all()
    raise_exception = False
    template_name = "portfolio/files/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = MediaSourceFile.objects.filter().get(pk=self.kwargs["pk"])
        return super().get_context_data(**kwargs)


class SourceFileCreateView(
    CreateView, HtmxView, PortfolioProfileMixin, LoginRequiredMixin
):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {"title": "New File"}
    fields = ["file"]
    http_method_names = ["get", "post", "delete"]
    login_url = reverse_lazy("login")
    model = MediaSourceFile
    partial_template_name = "portfolio/files/partials/_create.html"
    permission_denied_message = "Please login and try again."
    raise_exception = False
    success_url = reverse_lazy("list files")
    template_name = "portfolio/files/create.html"
    queryset = MediaSourceFile.objects.all()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = None
        return super().get_context_data(**kwargs)

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponse(status=200 if request.headers.get("HX-Request") else 403)


class SourceFileDeleteView(
    DeleteView, HtmxView, PortfolioProfileMixin, LoginRequiredMixin
):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {"title": "Delete File"}
    fields = ["file"]
    http_method_names = ["post"]
    login_url = reverse_lazy("login")
    model = MediaSourceFile
    partial_template_name = "portfolio/files/partials/_delete.html"
    permission_denied_message = "Please login and try again."
    queryset = MediaSourceFile.objects.all()
    raise_exception = False
    template_name = "portfolio/files/delete.html"
    success_url = reverse_lazy("list files")


class SourceFileUpdateView(
    UpdateView, HtmxView, PortfolioProfileMixin, LoginRequiredMixin
):
    content_type = "text/html"
    context_object_name = "file"
    extra_context = {"title": "Update File"}
    fields = ["file"]
    http_method_names = ["get", "post", "delete"]
    login_url = reverse_lazy("login")
    partial_template_name = "portfolio/files/partials/_update.html"
    permission_denied_message = "Please login and try again."
    raise_exception = False
    success_url = reverse_lazy("list files")
    template_name = "portfolio/files/update.html"
    model = MediaSourceFile
    queryset = MediaSourceFile.objects.all()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = MediaSourceFile.objects.filter().get(pk=self.kwargs["pk"])
        return super().get_context_data(**kwargs)

    def get_success_url(self, file: MediaSourceFile | None = None) -> str:
        if file is not None:
            return file.get_absolute_url()
        return str(self.success_url)


class SourceFileListView(ListView, HtmxView, PortfolioProfileMixin, LoginRequiredMixin):
    content_type = "text/html"
    context_object_name = "source_files"
    extra_context = {"title": "Files"}
    http_method_names = ["get", "post"]
    login_url = reverse_lazy("portfolio login")
    model = MediaSourceFile
    paginate_by = 25  # TODO: Implement pagination in default templates
    partial_template_name = "portfolio/files/partials/_list.html"
    permission_denied_message = "Please login and try again."
    queryset = MediaSourceFile.objects.all()
    raise_exception = False
    template_name = "portfolio/files/list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object_list = super().get_queryset()
        return super().get_context_data(**kwargs)
