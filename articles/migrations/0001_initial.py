# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug', max_length=100)),
                ('content', models.TextField(verbose_name='Contenu')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('views', models.IntegerField(default=0, verbose_name='Nombre de vues')),
                ('likes', models.IntegerField(default=0, verbose_name='Nombre de likes')),
                ('dislikes', models.IntegerField(default=0, verbose_name='Nombre de dislikes')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Auteur')),
            ],
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Contenu')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('article', models.ForeignKey(to='articles.Article', verbose_name='Article')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Auteur')),
            ],
        ),
    ]
