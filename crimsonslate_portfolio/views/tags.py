from django.views.generic import CreateView, UpdateView, DeleteView

from crimsonslate_portfolio.models import MediaTag
from crimsonslate_portfolio.views.mixins import HtmxTemplateResponseMixin


class TagCreateView(HtmxTemplateResponseMixin, CreateView):
    template_name = "crimsonslate_portfolio/tags/create.html"
    partial_template_name = "crimsonslate_portfolio/tags/partials/_create.html"
    model = MediaTag
    extra_context = {"class": "flex flex-col gap-4 p-4 border rounded bg-gray-200"}


class TagUpdateView(HtmxTemplateResponseMixin, UpdateView):
    template_name = "crimsonslate_portfolio/tags/update.html"
    partial_template_name = "crimsonslate_portfolio/tags/partials/_update.html"
    model = MediaTag
    extra_context = {"class": "flex flex-col gap-4 p-4 border rounded bg-gray-200"}


class TagDeleteView(HtmxTemplateResponseMixin, DeleteView):
    template_name = "crimsonslate_portfolio/tags/delete.html"
    partial_template_name = "crimsonslate_portfolio/tags/partials/_delete.html"
    model = MediaTag
    extra_context = {"class": "flex flex-col gap-4 p-4 border rounded bg-gray-200"}
