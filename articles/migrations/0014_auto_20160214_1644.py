# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_article_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='intro',
            field=models.TextField(verbose_name='Introduction'),
        ),
    ]
