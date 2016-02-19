# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20160115_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='content',
            field=models.TextField(error_messages={'blank': 'Votre commentaire est vide'}, verbose_name='Contenu'),
        ),
    ]
