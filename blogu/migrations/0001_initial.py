# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('views', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
                ('blog_content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('likes', models.IntegerField(default=0)),
                ('datetime_added', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id1', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('comment_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('comment_to', models.ForeignKey(to='blogu.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to=b'logo_images', blank=True)),
                ('date_registered', models.DateTimeField(null=True, blank=True)),
                ('address', models.CharField(max_length=300)),
                ('about', models.TextField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Discuss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discuss_text', models.TextField()),
                ('posted_on', models.DateTimeField(null=True, blank=True)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('intro', models.CharField(default=b'None', max_length=500)),
                ('started_on', models.DateTimeField(null=True, blank=True)),
                ('likes', models.IntegerField(default=0)),
                ('category', models.ForeignKey(to='blogu.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('followers', models.IntegerField(default=0)),
                ('no_followed', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('category', models.ForeignKey(to='blogu.Category')),
            ],
        ),
        migrations.CreateModel(
            name='UnPostedBlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('views', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
                ('text', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('datetime_added', models.DateTimeField(null=True, blank=True)),
                ('category', models.ForeignKey(to='blogu.Category')),
                ('written_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('picture', models.ImageField(default=b'media/profile_images/default.jpg', upload_to=b'profile_images')),
                ('level', models.IntegerField(default=1)),
                ('date_registered', models.DateTimeField(null=True, blank=True)),
                ('google_registered', models.BooleanField(default=False)),
                ('profile_tag_line', models.CharField(max_length=300, null=True, blank=True)),
                ('languages', models.IntegerField(default=1)),
                ('login', models.IntegerField(default=0)),
                ('dob_date', models.IntegerField(default=1)),
                ('dob_month', models.IntegerField(default=1)),
                ('dob_year', models.IntegerField(default=2000)),
                ('followed_tags', models.ManyToManyField(to='blogu.Tag', blank=True)),
                ('liked_blogs', models.ManyToManyField(to='blogu.Blog', blank=True)),
                ('liked_categories', models.ManyToManyField(to='blogu.Category', blank=True)),
                ('liked_comments', models.ManyToManyField(to='blogu.Comment', blank=True)),
                ('liked_discusses', models.ManyToManyField(to='blogu.Discuss', blank=True)),
                ('liked_discussions', models.ManyToManyField(to='blogu.Discussion', blank=True)),
                ('myreading_list', models.ManyToManyField(to='blogu.BlogId', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='follow',
            name='followed',
            field=models.ManyToManyField(to='blogu.UserProfile'),
        ),
        migrations.AddField(
            model_name='follow',
            name='userprofile',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discussion',
            name='started_by',
            field=models.ForeignKey(to='blogu.UserProfile'),
        ),
        migrations.AddField(
            model_name='discuss',
            name='discuss_by',
            field=models.ForeignKey(to='blogu.UserProfile'),
        ),
        migrations.AddField(
            model_name='discuss',
            name='discuss_on',
            field=models.ForeignKey(to='blogu.Discussion'),
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(to='blogu.Category'),
        ),
        migrations.AddField(
            model_name='blog',
            name='written_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
