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
        user_orgs = user.OrgUserRelationship.all().values_list(
                'organization_id',
                flat=True
            )
        kwargs["org_articles"] = Article.objects.filter(
             organizationarticle__organization__id__in=user_orgs
         )
        kwargs["shared_articles"] = Article.objects.filter(
            usersarticle__user=user
        )
        return kwargs
