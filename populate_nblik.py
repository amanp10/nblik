import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','paradox.settings')
import django
from django.contrib.auth.models import User
from datetime import datetime,date,tzinfo,timedelta
django.setup()

from nblik.models import Category,Blog,Comment

ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

utc = UTC()

def populate():
    user1=add_user(username='ankit',email='ankit@gmail.com',password='ankit')
    #user2=User.objects.get_or_create(username='nitingera1996',password='geranitin18091996')

    literature_cat = add_cat(name='Literature',likes=10)

    book_cat = add_cat(name="Books",likes=32)
	
    frame_cat = add_cat(name="History",likes=16)
	education_cat = add_cat(name="Education",likes=0,)
    _cat = add_cat(name="Incredible India",likes=0)
    _cat = add_cat(name="Automobiles",likes=0)
    _cat = add_cat(name="Interior Designing",likes=0)
    _cat = add_cat(name="Politics",likes=0)
    _cat = add_cat(name="Energy",likes=0)
    _cat = add_cat(name="Writing",likes=0)
    _cat = add_cat(name="Computer Science",likes=0)
    _cat = add_cat(name="Food & Cooking",likes=0)
    _cat = add_cat(name="Health",likes=0)
    _cat = add_cat(name="TV Serials",likes=0)
    _cat = add_cat(name="Economics",likes=0)
    _cat = add_cat(name="Relationships",likes=0)
    _cat = add_cat(name="International Relations",likes=0)
    _cat = add_cat(name="Journalism",likes=0)
    _cat = add_cat(name="Constitution",likes=0)
    _cat = add_cat(name="Kids World",likes=0)
    _cat = add_cat(name="Movies",likes=0)
    _cat = add_cat(name="Reviews",likes=0)
    _cat = add_cat(name="Entrepreneurship",likes=0)
    _cat = add_cat(name="Sports",likes=0)
    _cat = add_cat(name="Travel",likes=0)
    _cat = add_cat(name="How Tos",likes=0)
    _cat = add_cat(name="Science & Reserch",likes=0)
    _cat = add_cat(name="Gear & Gadgets",likes=0)
    _cat = add_cat(name="Hobbies & Fun",likes=0)
    _cat = add_cat(name="Psychology & Philosophy",likes=0)
    _cat = add_cat(name="Space",likes=0)
    _cat = add_cat(name="Others",likes=0)

#for c in Category.objects.all():
#    for b in Blog.objects.filter(category=c):
#        print "- {0} - {1}".format(str(c), str(b))

def add_blog(cat,title,blog_by,text,datetime_added,likes=0):
    b = Blog.objects.get_or_create(category=cat,title=title,written_by=blog_by,datetime_added=datetime_added)[0]
    b.text=text
    b.likes=likes
    b.save()
    return b

def add_cat(name,likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes=likes
    c.save()
    return c

def add_user(username,email,password):
    u=User.objects.get_or_create(username=username,email=email,password=password)[0]
    return u
#if __name__ == '__main__':
print "Starting nblik population script...."
populate() 	