# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nblik', '0016_auto_20160301_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.TextField(default=b'http://res.cloudinary.com/nblik/image/upload/icon.jpg'),
        ),
    ]
