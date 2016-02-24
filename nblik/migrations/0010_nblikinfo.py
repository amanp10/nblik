# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0009_auto_20160220_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='NblikInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heading', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('info', models.TextField()),
            ],
        ),
    ]
