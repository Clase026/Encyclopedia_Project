# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_string', models.CharField(max_length=255)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('username', models.CharField(max_length=255)),
                ('search', models.ForeignKey(to='search.Search')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='search',
            field=models.ForeignKey(to='search.Search'),
        ),
        migrations.AddField(
            model_name='article',
            name='search',
            field=models.ForeignKey(to='search.Search'),
        ),
    ]
