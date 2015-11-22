# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_article_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
