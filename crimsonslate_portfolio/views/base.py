from typing import Any

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

if not hasattr(settings, "PORTFOLIO_PROFILE"):
    raise ImproperlyConfigured("'PORTFOLIO_PROFILE' setting is required.")


class PortfolioProfileMixin(ContextMixin):
    """Adds :confval:`PORTFOLIO_PROFILE` to the view context."""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["profile"] = settings.PORTFOLIO_PROFILE
        return context


class HtmxTemplateView(TemplateView):
    """A template view that enables htmx features."""

    partial_template_name: str = ""
    """
    A partial template rendered by htmx.

    :type: :py:obj:`str`
    :value: ``""``

    """

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        """Sets :py:attr:`template_name` according to incoming headers ``HX-Request`` and ``HX-Boosted``."""
        htmx_request = bool(request.headers.get("HX-Request"))
        boosted = bool(request.headers.get("HX-Boosted"))

        if htmx_request and not boosted:
            self.template_name = self.partial_template_name
        return super().setup(request, *args, **kwargs)
