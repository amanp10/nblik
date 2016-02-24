# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0004_auto_20160218_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'media/profile_images/default.jpg', upload_to=b'profile_images'),
        ),
    ]
