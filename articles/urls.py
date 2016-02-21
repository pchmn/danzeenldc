from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_article$', views.create_article, name="create_article"),
    url(r'^$', views.get_articles, name="get_articles"),
    url(r'^(?P<page>\d+)', views.get_articles, name="get_articles"),
    url(r'^article/(?P<slug>[\w-]+)$', views.get_article, name="get_article"),
    url(r'^update/(?P<slug>[\w-]+)$', views.UpdateArticle.as_view(), name="update_article"),
    url(r'^delete/(?P<id>\d+)$', views.delete_article, name="delete_article"),
    url(r'^vote_article/(?P<id_article>\d+)', views.vote_article, name="vote_article"),
    url(r'^vote_comment/(?P<id_comment>\d+)', views.vote_comment, name="vote_comment"),
]