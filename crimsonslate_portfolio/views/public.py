from django.conf import settings
from django.contrib.auth.views import LoginView as LoginViewBase
from django.contrib.auth.views import LogoutView as LogoutViewBase
from django.urls import reverse_lazy

from crimsonslate_portfolio.forms import PortfolioAuthenticationForm
from crimsonslate_portfolio.views.base import HtmxView


class ContactView(HtmxView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Contact"}
    http_method_names = ["get", "post"]
    partial_template_name = "portfolio/partials/_contact.html"
    template_name = "portfolio/contact.html"


class LoginView(LoginViewBase, HtmxView):
    content_type = "text/html"
    extra_context = {"title": "Login", "profile": settings.PORTFOLIO_PROFILE}
    form_class = PortfolioAuthenticationForm
    http_method_names = ["get", "post"]
    partial_template_name = "portfolio/partials/_login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("list files")
    template_name = "portfolio/login.html"


class LogoutView(LogoutViewBase, HtmxView):
    content_type = "text/html"
    extra_context = {"title": "Logout", "profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post"]
    partial_template_name = "portfolio/partials/_logout.html"
    success_url = reverse_lazy("portfolio gallery")
    template_name = "portfolio/logout.html"
