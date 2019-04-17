from django.db import models
from wiki.models.article import Article
# Create your models here.


class ArticleType(models.Model):

    article = models.OneToOneField(Article, blank=True, null=True)
    public = models.BooleanField(default=False)
    shared_to_group = models.BooleanField(default=False)
    shared_to_organization = models.BooleanField(default=False)
