from django.utils.decorators import method_decorator
from django.views.generic.base import View
from wiki import models
from wiki.core.utils import object_to_json_response
from wiki.decorators import get_article
from django.db.models import Q


def get_all_chidren_of_an_org(matches, article_ids=[]):
    for m in matches:
        article_ids.append(m.id)
        if m.get_children() == 0:
            return m.id
        else:
            get_all_chidren_of_an_org(m.get_children(), article_ids)
    return article_ids


class QueryUrlPath(View):

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        user = request.user
        user_groups = user.GroupMemberRelation.all().values_list(
            'group__id',
            flat=True
        )
        user_orgs = user.OrgUserRelationship.all().values_list(
                'organization_id',
                flat=True
        )
        max_num = kwargs.pop('max_num', 20)
        query = request.GET.get('query', None)

        matches = []

        if query:
            matches = models.URLPath.objects.filter(
                Q(
                    article__organizationeditarticle__organization__id__in=user_orgs
                ) |
                Q(
                    article__organizationreadarticle__organization__id__in=user_orgs
                ) |
                Q(
                    article__groupeditarticle__group_id__in=user_groups
                ) |
                Q(
                    article__groupreadarticle__group_id__in=user_groups
                ) |
                Q(
                    article__usereditarticle__user=user
                ) |
                Q(
                    article__userreadarticle__user=user
                )
            )

            org_urlpath_ids = get_all_chidren_of_an_org(matches)

            # get the articles that the user has written 'article__owner=user'
            author_urlpath_ids = models.URLPath.objects.filter(article__owner=user).values_list('id', flat=True)

            queryset = models.URLPath.objects.filter(
                Q(id__in=org_urlpath_ids) | Q(id__in=author_urlpath_ids)
            ).distinct()

            active_user_matches = queryset.filter(article__current_revision__deleted=False)

            title_matches = active_user_matches.filter(
                article__current_revision__title__istartswith=query
            ).order_by('article__current_revision__title', 'article__current_revision__content', 'article__owner__name')

            content_matches = active_user_matches.filter(
                article__current_revision__content__icontains=query
            ).order_by('article__current_revision__title', 'article__current_revision__content', 'article__owner__name')

            author_matches = active_user_matches.filter(
                article__owner__name__istartswith=query
            ).order_by('article__current_revision__title', 'article__current_revision__content', 'article__owner__name')

            title_matches = title_matches.select_related_common()
            title_matches = [
                "[{title:s}](wiki:{url:s})".format(
                    title=m.article.current_revision.title,
                    url='/' + m.path.strip("/")
                # ) for m in matches[:max_num]
                ) for m in title_matches # no slicing to get all responses back
            ]

            content_matches = content_matches.select_related_common()
            content_matches = [
                "[{title:s}](wiki:{url:s})".format(
                    title=m.article.current_revision.title,
                    url='/' + m.path.strip("/")
                # ) for m in matches[:max_num]
                ) for m in content_matches # no slicing to get all responses back
            ]

            author_matches = author_matches.select_related_common()
            author_matches = [
                "[{title:s}](wiki:{url:s})".format(
                    title=m.article.current_revision.title,
                    url='/' + m.path.strip("/")
                # ) for m in matches[:max_num]
                ) for m in author_matches # no slicing to get all responses back
            ]

            matches = title_matches + content_matches + author_matches

            return object_to_json_response(matches)
