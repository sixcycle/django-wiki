from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from wiki.models.article import Article


class ArticleListView(GenericAPIView, ListModelMixin):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('owner__name', 'current_revision__title')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ArticleDetailView(GenericAPIView, RetrieveModelMixin):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
