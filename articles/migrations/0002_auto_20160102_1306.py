# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentaire',
            name='dislikes',
            field=models.IntegerField(verbose_name='Nombre de dislikes', default=0),
        ),
        migrations.AddField(
            model_name='commentaire',
            name='likes',
            field=models.IntegerField(verbose_name='Nombre de likes', default=0),
        ),
    ]
