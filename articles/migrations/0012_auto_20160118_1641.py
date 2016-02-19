# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_article_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='dislikes_width',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='likes_width',
            field=models.IntegerField(default=0),
        ),
    ]
