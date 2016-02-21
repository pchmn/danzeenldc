from django.contrib import admin
from django.core.urlresolvers import reverse

from articles.models import Article, Commentaire


class CommentsInline(admin.TabularInline):
    model = Commentaire
    extra = 0
    fields = ('content', 'author', 'date', 'likes', 'dislikes', 'score')
    readonly_fields = ('author', 'date', 'likes', 'dislikes', 'score')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    list_filter = ('author',)
    search_fields = ('title',)
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Général', {
            'fields': ('title', 'author', 'date', 'view_link'),
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
    readonly_fields = ('author', 'date', 'views', 'likes', 'dislikes', 'score', 'view_link')
    inlines = (CommentsInline,)

    def view_link(self, obj):
        """
        Retourne le lien vers l'article sur le site
        """
        return u"<a href='%s'>lien vers l'article</a>" % reverse("get_article", kwargs={'slug': obj.slug})

    view_link.short_description = "Lien vers l'article"
    view_link.allow_tags = True

admin.site.register(Article, ArticleAdmin)
