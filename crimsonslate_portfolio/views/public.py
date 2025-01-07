from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from crimsonslate_portfolio.forms import PortfolioAuthenticationForm


class DropzoneView(TemplateView):
    content_type = "text/html"
    template_name = "portfolio/dropzone.html"
    http_method_names = ["get", "post"]
    extra_context = {
        "class": "p-8 border-dashed border-4 border-gray-600/75",
        "button_class": "px-6 py-4 rounded bg-blue-500 hover:bg-blue-300",
    }


class ContactView(TemplateView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Contact"}
    http_method_names = ["get", "post"]
    partial_template_name = "portfolio/partials/_contact.html"
    template_name = "portfolio/contact.html"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.htmx_request = bool(request.headers.get("HX-Request"))
        if self.htmx_request:
            self.template_name = self.partial_template_name


class PortfolioLoginView(LoginView):
    content_type = "text/html"
    extra_context = {"title": "Login", "profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post"]
    template_name = "portfolio/login.html"
    partial_template_name = "portfolio/partials/_login.html"
    success_url = reverse_lazy("list files")
    redirect_authenticated_user = True
    form_class = PortfolioAuthenticationForm

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_template_name
        return super().setup(request, *args, **kwargs)


class PortfolioLogoutView(LogoutView):
    content_type = "text/html"
    extra_context = {"title": "Login", "profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post"]
    template_name = "portfolio/logout.html"
    partial_template_name = "portfolio/partials/_logout.html"
    success_url = reverse_lazy("portfolio gallery")

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_template_name
        return super().setup(request, *args, **kwargs)
