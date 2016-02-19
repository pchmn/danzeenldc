# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import articles.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0006_auto_20160111_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('votes_articles', articles.utils.JSONField()),
                ('votes_comments', articles.utils.JSONField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
