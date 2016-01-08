from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if(self.likes<0):
            self.likes=0
        super(Category, self).save(*args,**kwargs)

    def __unicode__(self):
	    return self.name

class Blog(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    written_by=models.ForeignKey(User)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    #content = RichTextField()
    blog_content=RichTextUploadingField()
    #comments=models.ManyToManyField(Comment)
    #text = models.TextField()
    likes=models.IntegerField(default=0)
    datetime_added=models.DateTimeField(default=datetime.now())
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if(self.likes<0):
            self.likes=0
        super(Blog, self).save(*args,**kwargs)

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    name=models.CharField(max_length=50)
    category=models.ForeignKey(Category)
    def __unicode__(self):
        return self.name

class Company(models.Model):
    user=models.OneToOneField(User)
    name=models.CharField(max_length=200)
    logo=models.ImageField(upload_to='logo_images',blank=True)
    date_registered=models.DateTimeField(default=datetime.now())
    address=models.CharField(max_length=300)
    about=models.TextField()
    def __unicode__(self):
        return self.name


class UnPostedBlog(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    written_by=models.ForeignKey(User)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    #comments=models.ManyToManyField(Comment)
    text = models.TextField()
    likes=models.IntegerField(default=0)
    datetime_added=models.DateTimeField(default=datetime.now())
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if(self.likes<0):
            self.likes=0
        super(Blog, self).save(*args,**kwargs)

    def __unicode__(self):
        return self.title

class BlogId(models.Model):
    id1=models.IntegerField()
    def __unicode__(self):
        return self.id1

class Discussion(models.Model):
    topic=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    intro=models.CharField(max_length=500,default="None")
    started_by=models.ForeignKey('blogu.UserProfile')
    started_on=models.DateTimeField(default=datetime.now())
    likes=models.IntegerField(default=0)
    category=models.ForeignKey(Category)
    def __unicode__(self):
        return self.topic
    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        if(self.likes<0):
            self.likes=0
        super(Discussion, self).save(*args,**kwargs)

class Discuss(models.Model):
    discuss_text=models.TextField()
    discuss_by=models.ForeignKey('blogu.UserProfile')
    discuss_on=models.ForeignKey(Discussion)
    posted_on=models.DateTimeField(default=datetime.now())
    likes=models.IntegerField(default=0)
    def __unicode__(self):
        return self.discuss_text

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='profile_images',default='media/profile_images/default.jpg')
    liked_blogs=models.ManyToManyField(Blog,blank=True)
    liked_categories=models.ManyToManyField(Category,blank=True)
    level=models.IntegerField(default=1)
    date_registered=models.DateTimeField(default=datetime.now())
    google_registered=models.BooleanField(default=False)
    profile_tag_line=models.CharField(max_length=300,null=True,blank=True)
    languages=models.IntegerField(default=1)#English=1,Hindi=2,English And Hindi both =3
    followed_tags=models.ManyToManyField(Tag,blank=True)
    login=models.IntegerField(default=0)#0=manual,1=google,2=facebook,3=linkedin,4=twitter
    dob_date = models.IntegerField(default=1)
    dob_month = models.IntegerField(default=1)
    dob_year = models.IntegerField(default=2000)
    myreading_list=models.ManyToManyField(BlogId,blank=True)
    liked_discussions=models.ManyToManyField(Discussion,blank=True)
    liked_discusses=models.ManyToManyField(Discuss,blank=True)
    liked_comments=models.ManyToManyField('blogu.Comment',blank=True)
    def __unicode__(self):
        return self.user.username

class Comment(models.Model):
    comment_text=models.TextField()
    comment_by=models.ForeignKey(User)
    comment_to=models.ForeignKey(Blog)
    likes=models.IntegerField(default=0)
    def __unicode__(self):
        return self.comment_text

class Follow(models.Model):
    userprofile=models.OneToOneField(User)
    followed=models.ManyToManyField(UserProfile)
    followers=models.IntegerField(default=0)
    no_followed=models.IntegerField(default=0)
    def __unicode__(self):
        return self.userprofile.username

