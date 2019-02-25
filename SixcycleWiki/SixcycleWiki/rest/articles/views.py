from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from wiki.models.article import Article
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    RetrieveModelMixin
)
from .serializers import ArticleSerializer


class ArticleListView(GenericAPIView, ListModelMixin):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ArticleDetailView(GenericAPIView, RetrieveModelMixin):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
