# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20160103_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=redactor.fields.RedactorField(verbose_name='Contenu'),
        ),
    ]
