from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    UpdateView,
    TemplateView,
    ListView,
    FormView,
)

from crimsonslate_portfolio.models import Media, MediaCategory
from crimsonslate_portfolio.forms import (
    MediaSearchForm,
    MediaUploadForm,
    PortfolioAuthenticationForm,
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
    login_url = reverse_lazy("portfolio login")

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
    login_url = reverse_lazy("portfolio login")

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.get_object().title
        return context


class PortfolioLoginView(LoginView):
    authentication_form = PortfolioAuthenticationForm
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Login"}
    http_method_names = ["get", "post"]
    template_name = "portfolio/login.html"


class PortfolioLogoutView(LogoutView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Logout"}
    http_method_names = ["get", "post"]
    success_url_allowed_hosts = settings.ALLOWED_HOSTS
    template_name = "portfolio/logout.html"


class PortfolioContactView(TemplateView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Contact"}
    http_method_names = ["get", "post"]
    template_name = "portfolio/contact.html"


class PortfolioGalleryView(ListView):
    content_type = "text/html"
    context_object_name = "medias"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Gallery"}
    http_method_names = ["get", "post"]
    model = Media
    ordering = "-date_created"
    paginate_by = 12
    queryset = Media.objects.filter(is_hidden__exact=False)
    template_name = "portfolio/gallery.html"


class PortfolioSearchView(TemplateView, FormView):
    context_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Search"}
    http_method_names = ["get", "post"]
    template_name = "portfolio/search.html"
    partial_template_name = "portfolio/search_results.html"
    form_class = MediaSearchForm
    success_url = reverse_lazy("portfolio search")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_template_name
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: MediaSearchForm) -> HttpResponse:
        results: QuerySet[Media, Media | None] = Media.objects.filter(
            Q(title__iexact=form.cleaned_data["title"])
            | Q(title__contains=form.cleaned_data["title"]),
        ).order_by("-date_created")

        if form.cleaned_data["categories"]:
            categories: list[int] = form.cleaned_data["categories"]
            results = results.filter(categories=categories)
        context: dict[str, Any] = self.get_context_data(results=results)
        return self.render_to_response(context=context)

    def get_context_data(
        self, results: QuerySet[Media, Media | None] | None = None, **kwargs
    ) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["results"] = results
        return context


class PortfolioUploadView(LoginRequiredMixin, FormView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Upload"}
    form_class = MediaUploadForm
    http_method_names = ["get", "post"]
    login_url = reverse_lazy("portfolio login")
    success_url = reverse_lazy("portfolio gallery")
    template_name = "portfolio/upload.html"

    def get_success_url(self, media: Media | None = None) -> str:
        if media is not None:
            return reverse("media detail", kwargs={"slug": media.slug})
        return reverse("portfolio gallery")

    def form_valid(self, form: MediaUploadForm) -> HttpResponseRedirect:
        media = Media.objects.create(
            source=form.cleaned_data["source"],
            thumb=form.cleaned_data["thumb"],
            title=form.cleaned_data["title"],
            subtitle=form.cleaned_data["subtitle"],
            desc=form.cleaned_data["desc"],
        )
        return HttpResponseRedirect(self.get_success_url(media))
