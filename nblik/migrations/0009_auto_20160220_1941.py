# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0008_auto_20160220_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(max_length=1500),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_tag_line',
            field=models.TextField(null=True, blank=True),
        ),
    ]
