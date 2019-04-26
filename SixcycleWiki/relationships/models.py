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


class OrganizationArticle(BaseArticleRelationship):
    # Represents an article that belongs to an organization,
    organization = models.ForeignKey(Organization)


class OrganizationReadArticle(BaseArticleRelationship):
    # Read permissions for an entire organization on
    # an article
    organization = models.ForeignKey(Organization)


class OrganizationEditArticle(BaseArticleRelationship):
    # Edit permissions for an entire organization on
    # an article
    organization = models.ForeignKey(Organization)


class GroupReadArticle(BaseArticleRelationship):
    # Read permissions for an entire group on
    # an article
    group = models.ForeignKey(Group)


class GroupEditArticle(BaseArticleRelationship):
    # Edit permissions for an entire group on
    # an article
    group = models.ForeignKey(Group)


class UserReadArticle(BaseArticleRelationship):
    # Read permissions for a user on
    # an article
    user = models.ForeignKey(User)


class UserEditArticle(BaseArticleRelationship):
    # Read permissions for a user on
    # an article
    user = models.ForeignKey(User)
