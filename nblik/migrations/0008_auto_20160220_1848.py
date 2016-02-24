# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0007_auto_20160220_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=imagekit.models.fields.ProcessedImageField(default=b'/static/images/icon.jpg', upload_to=b'profile_images'),
        ),
    ]
