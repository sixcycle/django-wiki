from django.db import models
from SixcycleWiki.authentication.models import (
    User,
    Organization,
    Group
)
from wiki.models.article import Article
# Create your models here.


class BaseArticleRelationship(models.Model):

    article = models.ForeignKey(Article)

    class Meta:
        abstract = True


class OrganizationReadArticle(BaseArticleRelationship):

    organization = models.ForeignKey(Organization)


class OrganizationEditArticle(BaseArticleRelationship):

    organization = models.ForeignKey(Organization)


class GroupReadArticle(BaseArticleRelationship):

    group = models.ForeignKey(Group)


class GroupEditArticle(BaseArticleRelationship):

    group = models.ForeignKey(Group)


class UserReadArticle(BaseArticleRelationship):

    user = models.ForeignKey(User)


class UserEditArticle(BaseArticleRelationship):

    user = models.ForeignKey(User)