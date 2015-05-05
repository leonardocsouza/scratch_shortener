# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='shorturl',
            field=models.CharField(db_index=True, unique=True, max_length=16, verbose_name=b'Short URL', blank=True),
        ),
    ]
