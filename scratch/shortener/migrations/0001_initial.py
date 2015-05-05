# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shortener.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shorturl', models.CharField(unique=True, max_length=16, verbose_name=b'Short URL', db_index=True)),
                ('httpurl', models.URLField(max_length=400, verbose_name=b'URL', validators=[shortener.models.validate_url])),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Create Date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name=b'Update Date')),
                ('is_vanity', models.BooleanField(default=False, verbose_name=b'Vanity URL?')),
            ],
        ),
        migrations.CreateModel(
            name='UrlStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('click_count', models.BigIntegerField(default=0, verbose_name=b'Click Count')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Create Date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name=b'Update Date')),
                ('url', models.OneToOneField(verbose_name=b'URL', to='shortener.Url')),
            ],
        ),
    ]
