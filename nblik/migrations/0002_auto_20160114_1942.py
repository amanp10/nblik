# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='intro',
            field=models.CharField(default=b'None', max_length=3000),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='topic',
            field=models.CharField(max_length=2000),
        ),
    ]
