# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20151122_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='search_string',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
