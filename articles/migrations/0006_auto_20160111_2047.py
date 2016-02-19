# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20160111_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentaire',
            name='score',
            field=models.IntegerField(verbose_name='Score', default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='Contenu'),
        ),
    ]
