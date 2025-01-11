from typing import Any
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from crimsonslate_portfolio.models import MediaSourceFile
from crimsonslate_portfolio.views.base import HtmxView


class SourceFileDetailView(DetailView, HtmxView, LoginRequiredMixin):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {"title": "File", "profile": settings.PORTFOLIO_PROFILE}
    fields = ["file"]
    http_method_names = ["get"]
    login_url = reverse_lazy("login")
    model = MediaSourceFile
    partial_template_name = "portfolio/files/partials/_detail.html"
    permission_denied_message = "Please login and try again."
    queryset = MediaSourceFile.objects.all()
    raise_exception = False
    template_name = "portfolio/files/detail.html"


class SourceFileCreateView(CreateView, HtmxView, LoginRequiredMixin):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {
        "title": "New File",
        "profile": settings.PORTFOLIO_PROFILE,  # TODO: Get class from profile
        "class": "p-4 bg-gray-800/45 border-4 border-dashed border-gray-500/80",
    }
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

    def get_success_url(self, file: MediaSourceFile | None = None) -> str:
        if file is not None:
            return reverse(file.get_absolute_url())
        return str(self.success_url)

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponse(status=200)


class SourceFileDeleteView(DeleteView, HtmxView, LoginRequiredMixin):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {"title": "Delete File", "profile": settings.PORTFOLIO_PROFILE}
    fields = ["file"]
    http_method_names = ["get", "post", "delete"]
    login_url = reverse_lazy("login")
    model = MediaSourceFile
    partial_template_name = "portfolio/files/partials/_delete.html"
    permission_denied_message = "Please login and try again."
    queryset = MediaSourceFile.objects.all()
    raise_exception = False
    success_url = reverse_lazy("delete file")
    template_name = "portfolio/files/delete.html"


class SourceFileUpdateView(UpdateView, HtmxView, LoginRequiredMixin):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {"title": "Update File", "profile": settings.PORTFOLIO_PROFILE}
    fields = ["file"]
    http_method_names = ["get", "post", "delete"]
    login_url = reverse_lazy("login")
    partial_template_name = "portfolio/files/partials/_update.html"
    permission_denied_message = "Please login and try again."
    raise_exception = False
    success_url = reverse_lazy("list files")
    template_name = "portfolio/files/update.html"


class SourceFileListView(ListView, HtmxView, LoginRequiredMixin):
    content_type = "text/html"
    context_object_name = "source_files"
    extra_context = {"title": "Files", "profile": settings.PORTFOLIO_PROFILE}
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
