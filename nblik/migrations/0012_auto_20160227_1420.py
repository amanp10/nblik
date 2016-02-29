# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0011_auto_20160224_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(unique=True, max_length=1500),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='slug',
            field=models.SlugField(unique=True, max_length=1500),
        ),
        migrations.AlterField(
            model_name='unpostedblog',
            name='slug',
            field=models.SlugField(unique=True, max_length=1500),
        ),
    ]
