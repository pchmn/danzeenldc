from django.contrib import admin
from articles.models import Article, Commentaire


class CommentsInline(admin.TabularInline):
    model = Commentaire
    extra = 0
    fields = ('content', 'author', 'date', 'likes', 'dislikes', 'score')
    readonly_fields = ('author', 'date', 'likes', 'dislikes', 'score')

# class CommentaireAdmin(admin.ModelAdmin):
#     fields = ('author', 'content')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    list_filter = ('author',)
    search_fields = ('title',)
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Général', {
            'fields': ('title', 'author', 'date'),
        }),
        # Fieldset 2 : contenu de l'article
        ('Contenu de l\'article', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ('intro', 'content')
        }),
       ('Infos', {
           'fields': ('views', 'likes', 'dislikes', 'score')
       })
    )
    readonly_fields = ('author', 'date', 'views', 'likes', 'dislikes', 'score')
    inlines = (CommentsInline,)

admin.site.register(Article, ArticleAdmin)
#admin.site.register(Commentaire, CommentaireAdmin)
