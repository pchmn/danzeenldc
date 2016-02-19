from django.contrib import admin
from articles.models import Article, Commentaire


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'intro', 'content', 'slug', 'author', 'likes', 'dislikes', 'views', 'score']


class CommentaireAdmin(admin.ModelAdmin):
    fields = ['author', 'content']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
