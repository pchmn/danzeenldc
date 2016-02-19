# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20160102_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='author',
            field=models.CharField(max_length=50, verbose_name='Auteur'),
        ),
    ]
