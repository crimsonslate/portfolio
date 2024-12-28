from datetime import datetime
from typing import Any
from uuid import uuid4

from boto3.session import Session
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import File
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    UpdateView,
    TemplateView,
    ListView,
    FormView,
)

from crimsonslate_portfolio.models import Media
from crimsonslate_portfolio.forms import (
    MediaSearchForm,
    MediaUploadForm,
)


class MediaDetailView(DetailView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post"]
    model = Media
    queryset = Media.objects.filter(is_hidden__exact=False)
    template_name = "portfolio/media/detail.html"

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.get_object().title
        return context


class MediaUpdateView(LoginRequiredMixin, UpdateView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    fields = ["source", "thumb", "title", "desc", "is_hidden"]
    http_method_names = ["get", "post"]
    model = Media
    template_name = "portfolio/media/edit.html"
    partial_name = "portfolio/media/_edit.html"
    login_url = reverse_lazy("portfolio login")

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_name
        return super().request(*args, **kwargs)

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.get_object().title
        return context


class MediaDeleteView(LoginRequiredMixin, DeleteView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post"]
    model = Media
    success_url = reverse_lazy("portfolio profile")
    template_name = "portfolio/media/delete.html"
    partial_name = "portfolio/media/_edit.html"
    login_url = reverse_lazy("portfolio login")

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_name
        return super().request(*args, **kwargs)

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.get_object().title
        return context


class ContactView(TemplateView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Contact"}
    http_method_names = ["get", "post"]
    template_name = "portfolio/contact.html"


class GalleryView(ListView):
    content_type = "text/html"
    context_object_name = "medias"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Gallery"}
    http_method_names = ["get", "post"]
    model = Media
    ordering = "-date_created"
    paginate_by = 12
    queryset = Media.objects.filter(is_hidden__exact=False)
    template_name = "portfolio/gallery.html"


class SearchView(FormView):
    allow_empty = True
    context_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Search"}
    http_method_names = ["get", "post"]
    template_name = "portfolio/search.html"
    partial_name = "portfolio/search_results.html"
    form_class = MediaSearchForm

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.headers.get("HX-Request"):
            self.__setattr__("template_name", self.partial_name)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: MediaSearchForm) -> HttpResponse:
        results: QuerySet = self.search_media(form)
        context: dict[str, Any] = self.get_context_data(results)
        return self.render_to_response(context)

    def get_context_data(
        self, results: QuerySet | None = None, **kwargs
    ) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["search_results"] = results
        return context

    def search_media(self, form: MediaSearchForm) -> QuerySet:
        results = Media.objects.filter(is_hidden=False)
        if form.cleaned_data["title"] != "*":
            results = results.filter(
                Q(title__contains=form.cleaned_data["title"])
                | Q(title__iexact=form.cleaned_data["title"])
            )
        return results


class UploadView(FormView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Upload"}
    http_method_names = ["get", "post"]
    login_url = reverse_lazy("login")
    form_class = MediaUploadForm
    success_url = reverse_lazy("upload complete")
    template_name = "portfolio/upload.html"

    def generate_upload_key(self) -> str:
        return str(uuid4())

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.boto3_session = Session().client("s3")
        self.upload_key = self.generate_upload_key()
        request.session["upload_key"] = self.upload_key

    def form_valid(self, form: MediaUploadForm) -> HttpResponseRedirect:
        file: File = form.cleaned_data["file"]
        response = self.boto3_session.create_multipart_upload(
            **{
                "Bucket": settings.PORTFOLIO_BUCKET_NAME,
                "ContentEncoding": "gzip",
                "ContentLanguage": "en-US",
                "ContentType": "multipart/form-data",
                "Key": self.upload_key,
            }
        )
        return super().form_valid(form=form)

    def get_success_url(self, boto3_response: dict | None = None) -> str:
        if not boto3_response:
            return super().get_success_url()
        return reverse(
            "upload part", kwargs={"upload_id": boto3_response.get("UploadId")}
        )


class UploadPartView(FormView):
    content_type = "text/html"
    form_class = MediaUploadForm
    http_method_names = ["post"]
    success_url = reverse_lazy("upload")
    template_name = "portfolio/upload_part.html"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.boto3_session = Session().client("s3")
        self.upload_key = request.session.get("upload_key")
        self.upload_id = self.kwargs.get("upload_id")
        self.part_id = self.kwargs.get("part_id")

    def form_valid(self, form: MediaUploadForm) -> HttpResponseRedirect:
        if not form.cleaned_data["upload_id"]:
            form.add_error("upload_id", ValidationError(_("No upload id provided.")))
            return self.form_invalid(form=form)

        file: File = form.cleaned_data["file"]
        upload_id: int = form.cleaned_data["upload_id"]
        chunk_size: int = form.cleaned_data.get("chunk_size", 256 * 2**10)
        chunks = file.chunks(chunk_size)
        parts: list = []
        for part_id, chunk in enumerate(chunks):
            part_response = self.boto3_session.upload_part(
                **{
                    "Body": chunk,
                    "UploadId": upload_id,
                    "PartNumber": part_id + 1,  # AWS parts start index at 1
                    "Bucket": settings.PORTFOLIO_BUCKET_NAME,
                    "ContentEncoding": "gzip",
                    "ContentLanguage": "en-US",
                    "ContentType": "multipart/form-data",
                    "Key": self.upload_key,
                }
            )
            parts.append(
                {
                    "ETag": part_response.get("ETag"),
                    "PartNumber": part_id,
                }
            )
        complete_response = self.boto3_session.complete_multipart_upload(
            **{
                "Bucket": settings.PORTFOLIO_BUCKET_NAME,
                "Key": self.upload_key,
                "UploadId": upload_id,
                "MultipartUpload": {
                    "Parts": parts,
                },
            }
        )
        media = self.create_media(response)
        return super().form_valid(form=form)

    def create_media(self, response: dict) -> Media:
        source_file: File = self.boto3_session.get_object(
            **{
                "Bucket": settings.PORTFOLIO_BUCKET_NAME,
                "IfMatch": True,
                "Key": response.get("Key"),
            }
        )
        return Media.objects.create(
            title=self.upload_key,
            source=source_file,
        )


class UploadProgressView(TemplateView):
    content_type = "text/html"
    http_method_names = ["get"]
    template_name = "portfolio/upload_progress.html"
