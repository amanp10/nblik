# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogu', '0061_auto_20151031_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='intro',
            field=models.CharField(default=b'None', max_length=500),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='liked_comments',
            field=models.ManyToManyField(to='blogu.Comment', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='liked_discusses',
            field=models.ManyToManyField(to='blogu.Discuss', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='liked_discussions',
            field=models.ManyToManyField(to='blogu.Discussion', blank=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='datetime_added',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='date_registered',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='discuss',
            name='posted_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='started_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='unpostedblog',
            name='datetime_added',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_registered',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='followed_tags',
            field=models.ManyToManyField(to='blogu.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='liked_blogs',
            field=models.ManyToManyField(to='blogu.Blog', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='liked_categories',
            field=models.ManyToManyField(to='blogu.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='myreading_list',
            field=models.ManyToManyField(to='blogu.BlogId', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'media/profile_images/default.jpg', upload_to=b'profile_images'),
        ),
    ]
