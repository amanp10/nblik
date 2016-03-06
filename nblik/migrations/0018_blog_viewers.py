# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0017_auto_20160304_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='viewers',
            field=models.ManyToManyField(to='nblik.UserProfile'),
        ),
    ]
