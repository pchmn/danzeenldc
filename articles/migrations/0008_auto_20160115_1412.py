# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='content',
            field=models.TextField(verbose_name='Contenu', error_messages={'required': 'Votre commentaire est vide'}),
        ),
    ]
