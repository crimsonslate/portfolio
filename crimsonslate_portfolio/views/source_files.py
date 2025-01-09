from django.conf import settings
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
from crimsonslate_portfolio.views.htmx import HtmxView


class SourceFileDetailView(LoginRequiredMixin, DetailView, HtmxView):
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


class SourceFileCreateView(LoginRequiredMixin, CreateView, HtmxView):
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
    queryset = MediaSourceFile.objects.all()
    raise_exception = False
    success_url = reverse_lazy("list files")
    template_name = "portfolio/files/create.html"


class SourceFileDeleteView(LoginRequiredMixin, DeleteView, HtmxView):
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


class SourceFileUpdateView(LoginRequiredMixin, UpdateView, HtmxView):
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


class SourceFileListView(LoginRequiredMixin, ListView, HtmxView):
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
