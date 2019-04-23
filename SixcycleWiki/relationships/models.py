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


class UsersArticle(BaseArticleRelationship):

    user = models.ForeignKey(User)


class OrganizationArticle(BaseArticleRelationship):

    organization = models.ForeignKey(Organization)


class GroupsArticle(BaseArticleRelationship):

    group = models.ForeignKey(Group)