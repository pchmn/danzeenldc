# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20160111_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=redactor.fields.RedactorField(verbose_name='Contenu Article'),
        ),
    ]
