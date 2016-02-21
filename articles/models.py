from django.core.validators import MaxLengthValidator
from django.db import models
from django.contrib.auth.models import User
from articles.utils import unique_slugify, JSONField


class UserProfile(models.Model):
    """
    Classe qui représente des informations supplémentaires
    pour un utilisateur
    """
    user = models.OneToOneField(User)
    votes_articles = JSONField()
    votes_comments = JSONField()


class Article(models.Model):
    """
    Classe qui représente un article
    Chaque article est lié à un utilisateur qui en est l'auteur
    """
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Slug")
    intro = models.TextField(verbose_name="Introduction")
    content = models.TextField(verbose_name="Contenu")
    author = models.ForeignKey(User, verbose_name="Auteur")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    views = models.IntegerField(default=0, verbose_name="Nombre de vues")
    likes = models.IntegerField(default=0, verbose_name="Nombre de likes")
    dislikes = models.IntegerField(default=0, verbose_name="Nombre de dislikes")
    score = models.IntegerField(default=0, verbose_name="Score")
    likes_width = models.IntegerField(default=0)
    dislikes_width = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        self.score = self.likes - self.dislikes
        if self.likes + self.dislikes > 0:
            self.likes_width = (self.likes / (self.likes + self.dislikes)) * 100
            self.dislikes_width = (self.dislikes / (self.likes + self.dislikes)) * 100
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return "article : %s" % self.title


class Commentaire(models.Model):
    """
    Classe qui représente les commentaires d'un article
    Chaque commentaire est lié à un article et à un utilisateur
    """
    content = models.TextField(verbose_name="Contenu", validators=[MaxLengthValidator(500)])
    author = models.CharField(max_length=50, verbose_name="Auteur")
    likes = models.IntegerField(default=0, verbose_name="Nombre de likes")
    dislikes = models.IntegerField(default=0, verbose_name="Nombre de dislikes")
    score = models.IntegerField(default=0, verbose_name="Score")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    article = models.ForeignKey(Article, verbose_name="Article")

    def save(self, *args, **kwargs):
        self.score = self.likes - self.dislikes
        super(Commentaire, self).save(*args, **kwargs)

    def __str__(self):
        return "commentaire : %s" % self.content


