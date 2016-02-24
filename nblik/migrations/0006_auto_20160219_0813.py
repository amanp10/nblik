# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0005_auto_20160218_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(unique=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='intro',
            field=models.TextField(default=b'None'),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='topic',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='unpostedblog',
            name='title',
            field=models.TextField(),
        ),
    ]
