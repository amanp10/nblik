# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0010_nblikinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='from_place',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lives_in',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='who',
            field=models.TextField(blank=True),
        ),
    ]
