from django import template
from nblik.models import Category,Blog,UserProfile,Follow
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('nblik/cats.html')
def get_category_list(cat=None):
    #print Category.objects.all()
    return {'cats':Category.objects.all().order_by('name'), "act_cat": cat}

@register.inclusion_tag('nblik/blogs.html')
def get_blogs_list(cat=None):
    if cat:
        c=Category.objects.get(slug=cat)
        if c:
            blogs=Blog.objects.filter(category=c).order_by('-likes')[:5]
    else:
        blogs=Blog.objects.order_by('-likes')[:5]
    return {'blogs':blogs}

@register.inclusion_tag('nblik/to_follow.html')
def get_to_follow_list(user=None):
    #print user
    if user:
        try:
            up=UserProfile.objects.get(user=user)
            up_follow=Follow.objects.get(userprofile=user)
            already_followed_list=up_follow.followed.all()
            liked_blog_list=up.liked_blogs.all()
            liked_categories_list=up.liked_categories.all()
            up_all=UserProfile.objects.all()
            up_list=[]
            for up1 in up_all:
                if up==up1:
                    continue
                if up1 in already_followed_list:
                    pass
                else:
                    up1_liked_blog_list=up1.liked_blogs.all()
                    #print up1_liked_blog_list
                    up1_liked_category_list=up1.liked_categories.all()
                    for lc1 in liked_categories_list:
                        if lc1 in up1_liked_category_list:
                            up_list.append(up1)
                            break
                        else:
                            for lb1 in liked_blogs_list:
                                if lb1 in up1_liked_blog_list:
                                    up_list.append(up1)
                                    break

            return {'userprofiles':up_list}
        except:
            return None
    else:
        return None
