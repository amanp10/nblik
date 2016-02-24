from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField


class Category(models.Model):
    name = models.CharField(max_length=1000,unique=True)
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
    title = models.TextField()
    written_by=models.ForeignKey(User)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    #content = RichTextField()
    blog_content=RichTextUploadingField()
    #comments=models.ManyToManyField(Comment)
    #text = models.TextField()
    likes=models.IntegerField(default=0)
    datetime_added=models.DateTimeField(null=True,blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if(self.likes<0):
            self.likes=0
        super(Blog, self).save(*args,**kwargs)

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    name=models.CharField(max_length=500)
    category=models.ForeignKey(Category)
    def __unicode__(self):
        return self.name

class Company(models.Model):
    user=models.OneToOneField(User)
    name=models.CharField(max_length=500)
    logo=models.ImageField(upload_to='logo_images',blank=True)
    date_registered=models.DateTimeField(null=True,blank=True)
    address=models.CharField(max_length=1500)
    about=models.TextField()
    def __unicode__(self):
        return self.name


class UnPostedBlog(models.Model):
    category = models.ForeignKey(Category)
    title = models.TextField()
    written_by=models.ForeignKey(User)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    #comments=models.ManyToManyField(Comment)
    text = models.TextField()
    likes=models.IntegerField(default=0)
    datetime_added=models.DateTimeField(null=True,blank=True)
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
    topic=models.TextField()
    slug=models.SlugField(unique=True)
    intro=models.TextField(default="None")
    started_by=models.ForeignKey('nblik.UserProfile')
    started_on=models.DateTimeField(null=True,blank=True)
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
    discuss_by=models.ForeignKey('nblik.UserProfile')
    discuss_on=models.ForeignKey(Discussion)
    posted_on=models.DateTimeField(null=True,blank=True)
    likes=models.IntegerField(default=0)
    def __unicode__(self):
        return self.discuss_text

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)
    picture = ProcessedImageField(upload_to='profile_images',processors=[ResizeToFill(300,300)],format='JPEG',options={'quality': 90},default='/static/images/icon.jpg')
    liked_blogs=models.ManyToManyField(Blog,blank=True)
    liked_categories=models.ManyToManyField(Category,blank=True)
    level=models.IntegerField(default=1)
    date_registered=models.DateTimeField(null=True,blank=True)
    google_registered=models.BooleanField(default=False)
    profile_tag_line=models.TextField(null=True,blank=True)
    languages=models.IntegerField(default=1)#English=1,Hindi=2,English And Hindi both =3
    followed_tags=models.ManyToManyField(Tag,blank=True)
    login=models.IntegerField(default=0)#0=manual,1=google,2=facebook,3=linkedin,4=twitter
    dob_date = models.IntegerField(default=1)
    dob_month = models.IntegerField(default=1)
    dob_year = models.IntegerField(default=2000)
    myreading_list=models.ManyToManyField(BlogId,blank=True)
    liked_discussions=models.ManyToManyField(Discussion,blank=True)
    liked_discusses=models.ManyToManyField(Discuss,blank=True)
    liked_comments=models.ManyToManyField('nblik.Comment',blank=True)
    from_place=models.TextField(blank=True)
    lives_in=models.TextField(blank=True)
    who=models.TextField(blank=True)
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
    followed=models.ManyToManyField(UserProfile,blank=True)
    followers=models.IntegerField(default=0)
    no_followed=models.IntegerField(default=0)
    def __unicode__(self):
        return self.userprofile.username

class NblikInfo(models.Model):
    heading=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    info=models.TextField()
    def __unicode__(self):
        return self.heading
    def save(self, *args, **kwargs):
        self.slug = slugify(self.heading)
        super(NblikInfo, self).save(*args,**kwargs)