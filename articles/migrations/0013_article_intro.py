# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20160118_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='intro',
            field=models.TextField(default='Intro par défaut, juste pour le test', verbose_name='Introduction'),
        ),
    ]
