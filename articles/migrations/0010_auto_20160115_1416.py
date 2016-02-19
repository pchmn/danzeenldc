# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_auto_20160115_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='content',
            field=models.TextField(verbose_name='Contenu'),
        ),
    ]
