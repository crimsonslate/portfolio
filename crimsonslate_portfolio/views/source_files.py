from django.http import HttpRequest, HttpResponse
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


class SourceFileDetailView(LoginRequiredMixin, DetailView):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {"title": "File", "profile": settings.PORTFOLIO_PROFILE}
    fields = ["file"]
    http_method_names = ["get"]
    template_name = "portfolio/files/detail.html"
    partial_template_name = "portfolio/files/partials/_detail.html"
    model = MediaSourceFile
    queryset = MediaSourceFile.objects.all()
    login_url = reverse_lazy("portfolio login")
    permission_denied_message = "Please login and try again."
    raise_exception = False


class SourceFileCreateView(CreateView):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {
        "title": "New File",
        "profile": settings.PORTFOLIO_PROFILE,
        "form_class": "p-8 mx-auto border-gray-600 border-dashed border-4 rounded-xl",
    }
    fields = ["file"]
    http_method_names = ["get", "post", "delete"]
    template_name = "portfolio/files/create.html"
    partial_template_name = "portfolio/files/partials/_create.html"
    success_url = reverse_lazy("portfolio files")
    model = MediaSourceFile
    queryset = MediaSourceFile.objects.all()
    login_url = reverse_lazy("portfolio login")
    permission_denied_message = "Please login and try again."
    raise_exception = False

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_template_name

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.headers.get("HX-Request"):
            return HttpResponse(status=403)
        return HttpResponse(b"", status=200)


class SourceFileDeleteView(DeleteView):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {"title": "Delete File", "profile": settings.PORTFOLIO_PROFILE}
    fields = ["file"]
    http_method_names = ["get", "post", "delete"]
    template_name = "portfolio/files/delete.html"
    partial_template_name = "portfolio/files/partials/_delete.html"
    success_url = reverse_lazy("delete file")
    model = MediaSourceFile
    queryset = MediaSourceFile.objects.all()
    login_url = reverse_lazy("portfolio login")
    permission_denied_message = "Please login and try again."
    raise_exception = False

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.htmx_request = bool(request.headers.get("HX-Request"))
        if self.htmx_request:
            self.template_name = self.partial_template_name

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.htmx_request:
            return HttpResponse(status=403)
        return HttpResponse(b"", status=200)


class SourceFileUpdateView(UpdateView):
    content_type = "text/html"
    context_object_name = "source_file"
    extra_context = {"title": "Update File", "profile": settings.PORTFOLIO_PROFILE}
    fields = ["file"]
    http_method_names = ["get", "post", "delete"]
    partial_template_name = "portfolio/files/partials/_update.html"
    success_url = reverse_lazy("update file")
    template_name = "portfolio/files/update.html"
    login_url = reverse_lazy("portfolio login")
    permission_denied_message = "Please login and try again."
    raise_exception = False

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.htmx_request = bool(request.headers.get("HX-Request"))
        if self.htmx_request:
            self.template_name = self.partial_template_name

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.htmx_request:
            return HttpResponse(status=403)
        return HttpResponse(b"", status=200)


class SourceFileListView(LoginRequiredMixin, ListView):
    content_type = "text/html"
    context_object_name = "source_files"
    extra_context = {"title": "Files", "profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post"]
    model = MediaSourceFile
    queryset = MediaSourceFile.objects.all()
    login_url = reverse_lazy("portfolio login")
    permission_denied_message = "Please login and try again."
    raise_exception = False
    template_name = "portfolio/files/list.html"
    partial_template_name = "portfolio/files/partials/_list.html"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_template_name
        return super().setup(request, *args, **kwargs)
