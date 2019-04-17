from django.shortcuts import render
from django.views.generic.base import TemplateView
from wiki.models import Article
# Create your views here.


class DashboardView(TemplateView):

    template_name = "view.html"

    def dispatch(self, request, *args, **kwargs):
        kwargs["user"] = request.user
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # GET AVAILABLE SLUGS
        user = kwargs.get("user", None)
        kwargs["owned_articles"] = Article.objects.filter(owner=user)
        return kwargs
