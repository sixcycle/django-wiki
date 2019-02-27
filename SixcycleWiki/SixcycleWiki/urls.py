"""SixcycleWiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern
from SixcycleWiki.rest.articles.views import (
    ArticleListView,
    ArticleDetailView
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
urlpatterns += [
    url(r'^api/articles/(?P<pk>\d+)/$',
        ArticleDetailView.as_view()),
    url(r'^api/articles/', ArticleListView.as_view()),
]
urlpatterns += [
    url(r'^notifications/', get_nyt_pattern()),
    url(r'', get_wiki_pattern())
]