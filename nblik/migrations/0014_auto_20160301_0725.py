# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0013_auto_20160301_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name=b'image'),
        ),
    ]
