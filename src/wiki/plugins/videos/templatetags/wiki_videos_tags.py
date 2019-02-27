from django import template
from wiki.plugins.videos import models, settings

register = template.Library()


@register.filter
def videos_for_article(article):
    return models.Video.objects.filter(
        article=article, current_revision__deleted=False).order_by(
        '-current_revision__created')


@register.filter
def videos_can_add(article, user):
    if not settings.ANONYMOUS and (not user or user.is_anonymous):
        return False
    return article.can_write(user)
