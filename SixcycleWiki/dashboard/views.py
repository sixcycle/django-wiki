from django.shortcuts import render
from django.views.generic.base import TemplateView
from wiki.models import Article, URLPath
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from SixcycleWiki.authentication.models import Organization
from dashboard.models import OrganizationAdmins
from relationships.models import *
from django.db.models import Q
from .values import CONTENT_PLACEHOLDER_USER_WIKI
# Create your views here.


class DashboardView(TemplateView):

    template_name = "view.html"

    def dispatch(self, request, *args, **kwargs):
        kwargs["user"] = request.user
        if request.user.is_anonymous():
            return redirect(to="/wiki/_accounts/login/?next=/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # GET AVAILABLE SLUGS
        user = kwargs.get("user", None)
        if user.is_anonymous:
            return kwargs
        user_orgs = user.OrgUserRelationship.all().values_list(
                'organization_id',
                flat=True
            )
        user_groups = user.GroupMemberRelation.all().values_list(
            'group__id',
            flat=True
        )

        # Collections is a list of tuples, where the first element is
        # the value of 'get_absolute_url', the second element is a specialized
        # string representation of the collection. In the case for
        # organizatinos it is the organizations name, in the case for User
        # collections, it is simply the article's title.
        collections = []
        for article in Article.objects.filter(
            organizationeditarticle__organization__id__in=user_orgs,
            is_root=True
                ):
            collections.append(
                (
                    article.get_absolute_url(),
                    str(article.organizationeditarticle_set.filter(
                        organization__id__in=user_orgs).first().organization))
            )
        for article in Article.objects.filter(
            organizationreadarticle__organization__id__in=user_orgs,
            is_root=True
                ):
            collections.append(
                (
                    article.get_absolute_url(),
                    str(article.organizationreadarticle_set.filter(
                        organization__id__in=user_orgs).first().organization)
                )
            )

        kwargs["collections"] = list(set(collections))

        if Article.objects.filter(owner=user, is_root=True).exists():
            kwargs["my_article"] = Article.objects.filter(owner=user, is_root=True).first()
        else:
            kwargs["my_article"] = "/myarticles"

        kwargs["shared_articles"] = Article.objects.filter(
            Q(
                organizationeditarticle__organization__id__in=user_orgs
            ) |
            Q(
                organizationreadarticle__organization__id__in=user_orgs
            ) |
            Q(
                groupeditarticle__group_id__in=user_groups
            ) |
            Q(
                groupreadarticle__group_id__in=user_groups
            ) |
            Q(
                usereditarticle__user=user
            ) |
            Q(
                userreadarticle__user=user
            )
        ).exclude(
            is_root=True
        )
        return kwargs


def my_article_view(request):
    user = request.user
    user_root_article = Article.objects.filter(
        owner=user,
        is_root=True
    ).first()
    if not user_root_article:
        new_path = URLPath.create_urlpath(
            parent=URLPath.root(),
            slug='my-articles-{}'.format(
                user.id
            ),
            title="My Articles",
            request=request,
            article_kwargs={"owner": user, "is_root": True},
            content=CONTENT_PLACEHOLDER_USER_WIKI
        )
        new_path.article.is_root = True
        new_path.article.save()
        return redirect(to=new_path.article.get_absolute_url())
    else:
        return redirect(to=user_root_article.get_absolute_url())
    return redirect(to="/dashboard")


def create_org_root_view(request):
    # TODO: Add better error handling
    org_id = request.GET.get("org_id", None)
    user = request.user
    if not user.is_superuser:
        return HttpResponseForbidden()
    org_root_article = Article.objects.filter(
        organizationarticle__organization_id=int(org_id),
        is_root=True
    ).first()
    if not org_root_article:
        org = Organization.objects.get(id=int(org_id))
        new_path = URLPath.create_urlpath(
            parent=URLPath.root(),
            slug='{}-resources'.format(
                org.name.replace(" ", "-")
            ),
            title="Resources",
            request=request,
            article_kwargs={"owner": user, "is_root": True},
            content=CONTENT_PLACEHOLDER_USER_WIKI
        )
        new_path.article.is_root = True
        new_path.article.save()
        org_article = OrganizationArticle(
            organization=Organization.objects.get(id=int(org_id)),
            article=new_path.article
        )
        org_article.save()
        org_admin = OrganizationAdmins(
            user=user,
            organization=org
        )
        org_admin.save()
        return redirect(to=new_path.article.get_absolute_url())
    else:
        return redirect(to=org_root_article.get_absolute_url())
    return HttpResponseForbidden()
