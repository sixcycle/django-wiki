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
from wiki.plugins.links.mdx.urlize import URLIZE_RE
import re
# Create your views here.


class DashboardView(TemplateView):

    template_name = "view.html"

    def parse_link_for_article(self, article):
        # Really sorry i had to do it this way, super pressed for time
        # Anything that isn't a square closing bracket
        name_regex = "[^]]+"
        # http:// or https:// followed by anything but a closing paren
        url_regex = "http[s]?://[^)]+"

        wiki_regex = "wiki:[^)]+"

        markup_regex = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)
        markup_wiki_regex = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, wiki_regex)

        contents = []
        for match in re.findall(markup_regex, article.current_revision.content):
            contents.append(match)

        for match in re.findall(markup_wiki_regex, article.current_revision.content):
            parsed_match = (match[0], "wiki" + match[1].replace("wiki:", "") + "/")
            contents.append(parsed_match)
        return contents

    def dispatch(self, request, *args, **kwargs):
        kwargs["user"] = request.user
        if request.user.is_anonymous():
            return redirect(to="/wiki/_accounts/login/?next=/")
        if not request.user.allowedusers_set.exits():
            return HttpResponseForbidden()
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

        final = dict()
        org_root_articles = Article.objects.filter(
            Q(
                organizationeditarticle__organization__id__in=user_orgs,
                is_root=True
            ) |
            Q(
                organizationreadarticle__organization__id__in=user_orgs,
                is_root=True
            )
        )

        for article in org_root_articles:
            org = None
            if article.organizationreadarticle_set.filter(
                    article__is_root=True, organization__id__in=user_orgs
                    ).exists():
                org = article.organizationreadarticle_set.filter(
                        article__is_root=True, organization__id__in=user_orgs
                    ).first().organization
            elif article.organizationeditarticle_set.filter(
                    article__is_root=True, organization__id__in=user_orgs
                    ).exists():
                org = article.organizationreadarticle_set.filter(
                        article__is_root=True, organization__id__in=user_orgs
                    ).first().organization
            final[org] = [
                {
                    child.article: self.parse_link_for_article(child.article)
                } for child in article.get_children()
            ]

        kwargs['collections'] = final

        if Article.objects.filter(owner=user, is_root=True).exists():
            my_article = Article.objects.filter(owner=user, is_root=True).first()
            kwargs["my_article"] = (
                my_article,
                self.parse_link_for_article(my_article)
            )
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
    if not request.user.allowedusers_set.exits():
        return HttpResponseForbidden()
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
    try:
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
                title="Articles",
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
    except Exception as ex:
        print("EXCEPTION IN CREATE OR ROOT IS {}".format(
            ex
        ))
