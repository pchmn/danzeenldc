from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from jsonfield import JSONField
from django.db.models.signals import post_save


class UserProfile(models.Model):
    """
    Classe qui représente des informations supplémentaires
    pour un utilisateur
    """
    user = models.OneToOneField(User, related_name="profile")
    views_articles = JSONField(verbose_name="Articles vues", default={}, blank=True)
    votes_articles = JSONField(verbose_name="Articles votés", default={}, blank=True)
    votes_comments = JSONField(verbose_name="Commentaires votés", default={}, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    """
    fonction qui crée un profile lorsqu'un utilisateur est créé
    """
    UserProfile.objects.get_or_create(user=instance)
