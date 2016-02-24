# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0002_auto_20160114_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followed',
            field=models.ManyToManyField(to='nblik.UserProfile', blank=True),
        ),
    ]
