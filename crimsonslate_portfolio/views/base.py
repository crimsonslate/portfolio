from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin


class PortfolioProfileMixin(ContextMixin):
    """Adds :confval:`PORTFOLIO_PROFILE` to the view context."""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["profile"] = settings.PORTFOLIO_PROFILE
        return context


class HtmxView(TemplateView):
    """Enables htmx features."""

    partial_template_name: str = ""
    """
    A partial template to be rendered by HTMX.

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
