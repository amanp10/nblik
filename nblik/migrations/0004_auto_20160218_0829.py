# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0003_auto_20160115_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'media/profile_images/default.jpg', width_field=b'100', upload_to=b'profile_images'),
        ),
    ]
