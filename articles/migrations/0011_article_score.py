# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_auto_20160115_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='score',
            field=models.IntegerField(verbose_name='Score', default=0),
        ),
    ]
