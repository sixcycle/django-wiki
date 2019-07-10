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
            # print("matches are {}".format(
            #     matches
            # ))
            matches = models.URLPath.objects.can_read(
                request.user).active().filter(
                Q(article__current_revision__title__icontains=query, article__current_revision__deleted=False) | # title
                Q(article__current_revision__content__icontains=query, article__current_revision__deleted=False) | # content
                Q(article__owner__name__icontains=query, article__current_revision__deleted=False) # authors name
            ).order_by('article__current_revision__title', 'article__current_revision__content', 'article__owner__name')
            # print("matches are {}".format(
            #     matches
            # ))
            matches = matches.select_related_common()
            matches = [
                "[{title:s}](wiki:{url:s})".format(
                    title=m.article.current_revision.title,
                    url='/' + m.path.strip("/")
                # ) for m in matches[:max_num]
                ) for m in matches # no slicing to get all responses back
            ]

        return object_to_json_response(matches)
