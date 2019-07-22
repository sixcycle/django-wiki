from django.utils.decorators import method_decorator
from django.views.generic.base import View
from wiki import models
from wiki.core.utils import object_to_json_response
from wiki.decorators import get_article
from django.db.models import Q


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
                ) |
                Q(
                    article__owner=user
                )
            )

            active_user_matches = models.URLPath.objects.can_read(request.user).active()

            title_matches = active_user_matches.filter(
                article__current_revision__title__istartswith=query, article__current_revision__deleted=False
            ).order_by('article__current_revision__title', 'article__current_revision__content', 'article__owner__name')

            content_matches = active_user_matches.filter(
                article__current_revision__content__icontains=query, article__current_revision__deleted=False
            ).order_by('article__current_revision__title', 'article__current_revision__content', 'article__owner__name')

            author_matches = active_user_matches.filter(
                article__owner__name__istartswith=query, article__current_revision__deleted=False
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
