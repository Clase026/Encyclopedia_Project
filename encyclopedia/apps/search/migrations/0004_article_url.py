# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_tweet_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
