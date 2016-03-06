from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpRequest
from nblik.models import Category,Blog,UserProfile,Comment,Follow,Discussion,Discuss,Tag,NblikInfo
from nblik.forms import BlogForm
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.models import User
from datetime import datetime,date,tzinfo,timedelta
from collections import Counter
import json
import facebook
from unidecode import unidecode
import cloudinary
import cloudinary.uploader
import cloudinary.api

ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

utc = UTC()

class MyRegistrationView(RegistrationView):
    def get(self):
        print self

def modify_content(blog_id):
    b=Blog.objects.get(id=int(blog_id))
    str1=b.blog_content
    repeat=0
    if str1.find('src="/media/blog_uploads')!= -1:
        repeat=1
        i1=str1.find('src="/media/')
        #print i1
        i2=str1.find('/media/blog_uploads/')
        i4=str1.find('style=',i1)
        i3=str1.rfind('.',i2,i4)
        #print i2
        #print i3
        str2=str1[i2+20:i3+5].replace('"','')
        str3=str1[i1+5:i3+5].replace('"','')
        #print str2
        #print str3
        context_dict1=cloudinary.uploader.upload('/static/media/blog_uploads/'+str2,public_id='blog_uploads/'+str2,width = 700, height = 700, crop = 'limit')
        url=context_dict1['url']
        #url='http://res.cloudinary.com/nblik/image/upload/blog_uploads/'+str2 ##
        str4=str1.replace(str3,url)
        #print str4
        b.blog_content=str4
        b.save()
    if repeat==1:
        modify_content(blog_id)

def index(request):
    if request.method=="POST":
        blog_text=request.POST.get('blog_text')
        return render(request,'nblik/add_blog.html',{'blog_text':blog_text})
    if request.user.is_active:
        blog_list = Blog.objects.order_by('-id')[:25]
    else:
        blog_list = Blog.objects.order_by('-id')[:10]
    show=[True]*len(blog_list)
    try:
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        liked_blogs_list=user2.liked_blogs.all()
        ##print len(blog_list)
        for i in range(0,len(blog_list)):
            for lb in liked_blogs_list:
                if lb == blog_list[i]:
                    show[i]=False
                    break
                else:
                    show[i]=True
    except:
        pass
    context_dict = {}
    ##print datetime.now()
    ##print show
    context_dict['blogs']=blog_list
    comment_matrix=[]
    comments_number={}
    for blog in blog_list:
        comment_matrix.append(Comment.objects.filter(comment_to=blog).order_by('-likes')[:5])
        comments_number[blog.title]=len(Comment.objects.filter(comment_to=blog))
    context_dict['comments']=comment_matrix
    context_dict['comments_number']=comments_number
    b_time=[]
    for b in blog_list:
        days=(datetime.now(utc)-b.datetime_added).days
        seconds=(datetime.now(utc) - b.datetime_added).seconds
        minutes=seconds/60
        hours=minutes/60
        if  days>= 1:
            b_time.append(str(days)+" days ago")
        elif minutes>60:
            b_time.append(str(hours)+" hours ago")
        elif seconds>60:
            b_time.append(str(minutes)+" minutes ago")
        else:
            b_time.append("Just now")
    zipped_data=zip(blog_list,b_time,show)
    context_dict['zipped_data']=zipped_data
    #context_dict['u']=user1
    response = render(request,'nblik/index.html',context_dict)
    return response

def profile(request):
	pass

def category(request,category_name_slug):

    context_dict = {}
    context_dict['result_list']=None
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name']=category.name
        if request.user.is_active:
            blog_list = Blog.objects.filter(category=category).order_by('-id')
        else:
            blog_list = Blog.objects.filter(category=category).order_by('-id')[:10]
        context_dict['category']=category
        context_dict['category_name_slug']=category.slug
        show=[True]*len(blog_list)
        try:
            user1=User.objects.get(username=request.user)
            user2=UserProfile.objects.get(user=user1)
            liked_blogs_list=user2.liked_blogs.all()
            ##print len(blog_list)
            for i in range(0,len(blog_list)):
                for lb in liked_blogs_list:
                    if lb == blog_list[i]:
                        show[i]=False
                        break
                    else:
                        show[i]=True
            show_cat="yes"
            for cat in user2.liked_categories.all():
                if cat == category:
                    show_cat=None
                    break
        except:
            show_cat=None
        b_time=[]
        comments_number={}
        for b in blog_list:
            comments_number[b.title]=len(Comment.objects.filter(comment_to=b))
            days=(datetime.now(utc)-b.datetime_added).days
            seconds=(datetime.now(utc) - b.datetime_added).seconds
            minutes=seconds/60
            hours=minutes/60
            if  days>= 1:
                b_time.append(str(days)+" days ago")
            elif minutes>60:
                b_time.append(str(hours)+" hours ago")
            elif seconds>60:
                b_time.append(str(minutes)+" minutes ago")
            else:
                b_time.append("Just now")
        context_dict['comments_number']=comments_number
        context_dict['show_cat']=show_cat
        zipped_data=zip(blog_list,b_time,show)
        context_dict['zipped_data']=zipped_data
    except Category.DoesNotExist:
        context_dict['category_name']=category_name_slug
    return render(request,'nblik/category.html',context_dict)


def get_category_list(max_results=0,startswith=''):
    cat_list=[]
    if startswith=='':
        cat_list = Category.objects.all()
    elif startswith:
        ##print "Hello"
        cat_list = Category.objects.filter(name__istartswith=startswith)
        ##print cat_list1
    if max_results>0:
        if len(cat_list)>max_results:
            cat_list=cat_list[:max_results]
    return cat_list

def blog(request,blog_title_slug):
    b=None
    c=None
    b_time=None
    b=Blog.objects.get(slug=blog_title_slug)
    viewer_list=b.viewers.all()
    b.views+=1
    for viewer in viewer_list:
        if viewer==request.user.userprofile:
            b.views-=1
            b.viewers.remove(viewer)
    b.viewers.add(request.user.userprofile)
    b.save()
    try:
        b=Blog.objects.get(slug=blog_title_slug)
        ##print b.blog_content
        c=Comment.objects.filter(comment_to=b).order_by('-likes')
        comments_number=len(c)
        comment_by_name=[]
        for co in c:
            u=co.comment_by
            up=UserProfile.objects.get(user=u)
            comment_by_name.append(up.name)
        comments=zip(c,comment_by_name)
    except Blog.DoesNotExist:
        pass
    ##print type(b.text)
    try:
        b=Blog.objects.get(slug=blog_title_slug)
        #print b.blog_content
        us=request.user
        up=UserProfile.objects.get(user=request.user)
        liked_comments=up.liked_comments.all()
        show=True
        show_comment={}
        for bl in up.liked_blogs.all():
            if bl==b:
                show=False
                break;
        for co in c:
            show_comment[co.id]="yes"
            for comment in liked_comments:
                if comment==co:
                    show_comment[co.id]=None
                    break
    except:
        up=None
        us=None
        show=None
        show_comment=None
    ##print show_comment
    days=(datetime.now(utc)-b.datetime_added).days
    seconds=(datetime.now(utc) - b.datetime_added).seconds
    minutes=seconds/60
    hours=minutes/60
    if  days>= 1:
        b_time=str(days)+" days ago"
    elif minutes>60:
        b_time=str(hours)+" hours ago"
    elif seconds>60:
        b_time=str(minutes)+" minutes ago"
    else:
        b_time="Just now"
    return render(request,'nblik/blog.html',{'blog':b,'comments':comments,'b_time':b_time,'show':show,'u':us,'up':up,'comments_number':comments_number,'show_comment':show_comment})

@login_required
def like_category(request):
    if request.method=="GET":
        category_id=request.GET["category_id"]
        category1=Category.objects.get(id=int(category_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        lke_list=user2.liked_categories.all()
        for lke in lke_list:
            if lke == category1:
                return HttpResponse(category1.likes)
        category1.likes+=1
        category1.save()
        user2.liked_categories.add(category1)
        user2.save()
        return HttpResponse(category1.likes)

def suggest_category(request):
    str=request.GET["query_string"]
    ##print str
    result=get_category_list(100,str)
    cat_list=[]
    for name in result:
        cat=Category.objects.get(name=name)
        cat_list.append(cat)
    ##print cat_list
    return render(request,'nblik/category_list.html',{'cats':cat_list})
    #return HttpResponse(cat_list)

@login_required
def like_blog(request):
    ##print "Hello"
    if request.method=="GET":
        blog_id=request.GET["blog_id"]
        blog=Blog.objects.get(id=int(blog_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        user_liked=user2.liked_blogs.all()
        for blg in user_liked:
            if blog == blg:
                return HttpResponse(blog.likes)
        user2.liked_blogs.add(blog)
        user2.save()
        blog.likes+=1
        blog.save()
        return HttpResponse(blog.likes)

@login_required
def like_discussion(request):
    ##print "Hello"
    if request.method=="GET":
        discussion_id=request.GET["discussion_id"]
        discussion=Discussion.objects.get(id=int(discussion_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        liked_discussions=user2.liked_discussions.all()
        for dis in liked_discussions:
            if dis == discussion:
                return HttpResponse(discussion.likes)
        discussion.likes+=1
        discussion.save()
        user2.liked_discussions.add(discussion)
        user2.save()
        return HttpResponse(discussion.likes)

@login_required
def like_discuss(request):
    ##print "Hello"
    if request.method=="GET":
        discuss_id=request.GET["discuss_id"]
        discuss=Discuss.objects.get(id=int(discuss_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        l_list=user2.liked_discusses.all()
        for lke in l_list:
            if lke == discuss:
                return HttpResponse(discuss.likes)
        discuss.likes+=1
        discuss.save()
        user2.liked_discusses.add(discuss)
        user2.save()
        return HttpResponse(discuss.likes)

@login_required
def like_comment(request):
    ##print "Hello"
    if request.method=="GET":
        comment_id=request.GET["comment_id"]
        comment=Comment.objects.get(id=int(comment_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        l_list=user2.liked_comments.all()
        for lke in l_list:
            if lke == comment:
                return HttpResponse(comment.likes)
        comment.likes+=1
        comment.save()
        user2.liked_comments.add(comment)
        user2.save()
        return HttpResponse(comment.likes)

def add_blog(request,category_name_slug):
    try:
        cat=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat=None

    if request.method=="POST":
        if cat:
            blog_content=request.POST['blog_content']
            blog_title=request.POST['blog_title']
            ##print type(blog_content)
            user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
            blog1=Blog.objects.get_or_create(title=blog_title,
                                        category=cat,
                                        written_by=request.user,
                                        likes=0,
                                        views=0,
                                        datetime_added=datetime.now(),
                                        text=blog_content
                                        )
            blog1=Blog.objects.get(title=blog_title)
            #blog1.save()
            #return HttpResponse('Hello')
            modify_content(blog1.id)
            return blog(request,blog1.slug)
    else:
        context_dict={'category_list':Category.objects.all(),'category':cat}
        return render(request,'nblik/add_blog.html',context_dict)

def add_blog2(request,category_name_slug):
    try:
        cat=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat=None

    if request.method=="POST":
        blog1=BlogForm(request.POST)
        if blog1.is_valid():
            title = blog1.cleaned_data['title']
            blog_content=blog1.cleaned_data['blog_content']
            #blog1.save(commit=False)
            blog1=Blog(title=title,blog_content=blog_content)
            blog1.datetime_added=datetime.now()
            blog1.category=cat
            blog1.written_by=request.user
            blog1.save()
            modify_content(blog1.id)
            return blog(request,blog1.slug)
        else:
            form=BlogForm()
            cat=None
            blog_list=Blog.objects.all()
            context_dict={'category_list':Category.objects.all(),'category':cat,'myform':form,'blog_list':blog_list}
            return render(request,'nblik/add_blog.html',context_dict)
    else:
        form=BlogForm()
        blog_list=Blog.objects.all()
        context_dict={'category_list':Category.objects.all(),'category':cat,'myform':form,'blog_list':blog_list}
        return render(request,'nblik/add_blog2.html',context_dict)

def create_signup_username(signup_name):
        u_list = UserProfile.objects.all()
        max1=1
        found=0
        for u in u_list:
            if u.name==signup_name:
                found=1
                prev_username=u.user.username
                lindex=prev_username.rfind("-",0,len(prev_username))
                s=Counter(prev_username)
                val=s['-']
                num=int(prev_username[lindex+1:])
                if num>max1:
                    max1=num
        if found==1:
            str_num=str(max1+1)
            str1 = prev_username[:lindex+1] + str(num+1)
        else:
            str1=slugify(signup_name)
            str1=str1+'-1'
        return str1

def login_and_signup(request):
    if request.method == 'POST':
        login_statement=None
        signup_statement=None
        login_username_or_email = request.POST.get('login_username_or_email')
        if login_username_or_email:
            login_password = request.POST.get('login_password')
            if not login_username_or_email:
                login_statement="Please enter the username"
            if not login_password and login_username_or_email:
                login_statement ="Please enter the password"
            try:
                u=User.objects.get(email=login_username_or_email)
                login_username=u.username
            except:
                login_username=login_username_or_email
            try:
                u=User.objects.get(username=login_username)
            except:
                u=None
            user = authenticate(username = login_username,password=login_password)
            if user and login_username and login_password:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect('/nblik/')
                else:
                    return HttpResponse("Your Nblik account is disabled.")
            else:
                #print "Invalid login details: {0}, {1}".format(login_username,login_password)
                login_statement="Invalid username password combination"
        else:
            registered = False
            signup_name = request.POST.get('signup_name')
            signup_email = request.POST.get('signup_email')
            signup_password1 = request.POST.get('signup_password1')
            signup_password2 = request.POST.get('signup_password2')
            register_as = request.POST.get('register_as')         
            try:
                u=User.objects.get(email=signup_email)
                signup_statement="Email already registered"
            except:
                if signup_password1!=signup_password2:
                    signup_statement="password not same"
                else:
                    signup_username=create_signup_username(signup_name)
                    user=User.objects.create_user(username=signup_username,email=signup_email)
                    user.set_password(signup_password1)
                    user.save()
                    user1=User.objects.get(username=signup_username)
                    if register_as=="user":
                        profile=UserProfile(user=user1,level=1)
                        profile.name=signup_name
                        profile.save()
                        up_follow=Follow(userprofile=user1)
                        up_follow.save()
                    else:
                        company=Company(user=user1)
                        company.name=signup_name
                        company.save()
                    user1 = authenticate(username = signup_username,password=signup_password1)
                    #user1 = authenticate(username = signup_username,password=signup_password1)
                    #print user1
                    login(request,user1)
                    cat_list=Category.objects.all()
                    return render(request,'nblik/next_step.html',{'email':signup_email,'name':signup_name,'cat_list':cat_list}) 
                    #return render(request,'nblik/signup2.html',{'username':signup_username})

        return render(request,'nblik/login.html',{'login_statement':login_statement,'signup_statement':signup_statement,'cat_list':Category.objects.all()})
    else:
        return render(request,'nblik/login.html',{})

def google_login(request):
    if request.method=="POST":
        ##print "Hello"
        email=request.POST['email']
        image_url=request.POST['image_url']
        name=request.POST['name']
        google_id=request.POST['id']
        response_dict={}
        #print "email=",email
        try:
            u=User.objects.get(email=email)
            up=UserProfile.objects.get(user=u)
            if up.google_registered:
                up.login=1
                up.save()
            else:
                up.google_id=google_id
                up.google_registered=True
                up.login=1
                up.save()
                    ##print "Hello"
            user = authenticate(username = up.user.username,password=up.user.password)
            if user:
                if user.is_active:
                    login(request,user)
                    response_dict.update({'response':"logged in"})
                    response=HttpResponse(json.dumps(response_dict), content_type='application/javascript')
                else:
                    response_dict.update({'response':"Your Nblik account is disabled."})
                    response=HttpResponse(json.dumps(response_dict), content_type='application/javascript')

        except:
            #print "In except"
            signup_username=create_signup_username(name)
            #print signup_username,email
            user=User.objects.create_user(username=signup_username,email=email)
            user.set_password("password")
            user.save()
            user1=User.objects.get(username=signup_username)
            #print "user1=", user1
            profile=UserProfile(user=user1,level=1)
            profile.name=name
            profile.google_id=google_id
            profile.google_registered=True
            profile.login=1
            profile.save()
            up_follow=Follow(userprofile=user1)
            up_follow.save()
            user1 = authenticate(username = signup_username,password="password")
            #user1 = authenticate(username = signup_username,password=signup_password1)
            login(request,user1)
            response_dict.update({'response':'logged_in'})
            response=HttpResponse(json.dumps(response_dict), content_type='application/javascript')
        return response


def search_top(request):
    q_str=request.GET["query_string"]
    ##print str
    result=get_category_list(100,q_str)
    cat_list=[]
    for name in result:
        cat=Category.objects.get(name=name)
        cat_list.append(cat)

    blog_list=Blog.objects.all()
    b_list=[]
    for blog in blog_list:
        title=blog.title
        for word in title.split():
            if word.lower().startswith(q_str.lower()):
                b_list.append(blog)
                break

    user_list = UserProfile.objects.all()
    u_list=[]
    for u in user_list:
        if u.name.lower().startswith(q_str.lower()):
           u_list.append(u)
    ##print cat_list,b_list,u_list
    ##print cat_list
    context_dict={}
    context_dict['cats']=cat_list
    context_dict['blogs']=b_list
    context_dict['users']=u_list
    ##print context_dict
    #return HttpResponse("Results")
    return render(request,"nblik/search_results.html", context_dict)

    #return HttpResponse(cat_list)

def user_logout(request):
    logout(request)
    #print "Hello"
    return HttpResponseRedirect('/nblik/')


def follow_user(request):
    if request.method=="GET":
        user_id=request.GET["user_id"]
        userprofile=UserProfile.objects.get(id=int(user_id))
        u=User.objects.get(username=userprofile.user.username)
        up_follow=Follow.objects.get(userprofile=u)
        current_up_follow=Follow.objects.get(userprofile=request.user)
        for follo in current_up_follow.followed.all():
            if userprofile==follo:
                return HttpResponse("NotFollowed")
        up_follow.followers=up_follow.followers+1
        current_up_follow.followed.add(userprofile)
        current_up_follow.no_followed=current_up_follow.no_followed+1
        current_up_follow.save()
        up_follow.save()
        return HttpResponse("followed")


def dashboard(request,username):
    context_dict={}
    show='yes'
    try:
        user_m=User.objects.get(username=username)
        userprofile=UserProfile.objects.get(user=user_m)
        blog_list=Blog.objects.filter(written_by=user_m)
        discussion_list=Discussion.objects.filter(started_by=userprofile)
        cat_list=userprofile.liked_categories.all()
        follow=Follow.objects.get(userprofile=request.user)
        for foll in follow.followed.all():
            if foll==userprofile:
                show=None
                break
    except:
        user_m=None
        userprofile=None
    try:
        followed_tags=userprofile.followed_tags.all()
    except:
        followed_tags=None
    try:
        userprofile_follow=Follow.objects.get(userprofile=user_m)
        followed_list=userprofile_follow.followed.all()
        followers=userprofile.follow_set.all()
    except:
        userprofile_follow=None
        followed_list=None
        followers=None
    if userprofile.languages == 1:
        lang='English'
    if userprofile.languages == 2:
        lang='Hindi'
    if userprofile.languages == 3:
        lang='English and Hindi'
    context_dict['show']=show
    context_dict['cat_list']=cat_list
    context_dict['user']=request.user
    context_dict['user_m']=user_m
    context_dict['userprofile']=userprofile
    context_dict['userprofile_follow']=userprofile_follow
    context_dict['followed_tags']=followed_tags
    context_dict['followed_list']=followed_list
    context_dict['followers']=followers
    context_dict['blogs']=blog_list
    context_dict['discussions']=discussion_list
    context_dict['lang']=lang
    context_dict['l_blogs']=len(blog_list)
    context_dict['l_dis']=len(discussion_list)
    return render(request,'nblik/dashboard.html',context_dict)

def comment(request):
    if request.method=="GET":
        ##print "Hello"
        blog_id=request.GET["blog_id"]
        ##print blog_id
        user_id=request.GET["user_id"]
        ##print user_id
        comment_text=request.GET["comment_text"]
        b=Blog.objects.get(id=int(blog_id))
        ##print b
        u=User.objects.get(id=int(user_id))
        ##print b,u
        c=Comment.objects.get_or_create(comment_text=comment_text,comment_by=u,comment_to=b,likes=0)
        return HttpResponse(0)

def discussions(request):
    if request.user.is_active:
        discussions=Discussion.objects.order_by('-id')
    else:
        discussions=Discussion.objects.order_by('-id')[:10]
    return render(request,'nblik/discussions.html',{'discussions':discussions})

def new_discussion(request):
    if request.method=='POST':
        user=request.user
        user_pro=UserProfile.objects.get(user=user)
        topic=request.POST.get('discuss_topic')
        intro=request.POST.get('discuss_intro').replace("\r\n","<br />").replace("\r","<br />").replace("\n","<br />")
        cat=request.POST.get('category')
        category=Category.objects.get(id=int(cat))
        discussion=Discussion(topic=topic,started_by=user_pro,category=category,intro=intro)
        discussion.save()
        discuss_list=discussion.discuss_set.all()
        return render(request,'nblik/discussion.html',{'discuss_list':discuss_list,'up':user_pro,'discussion':discussion})
    else:
        context_dict={}
        context_dict['categories']=Category.objects.all()
        return render(request,'nblik/new_discussion.html',context_dict)

def discussion(request,discussion_slug):
    d=Discussion.objects.get(slug=discussion_slug)
    discuss_list=d.discuss_set.all()
    up=UserProfile.objects.get(user=request.user)
    liked_discussions=up.liked_discussions.all()
    liked_discusses=up.liked_discusses.all()
    show="yes"
    show_discuss={}
    for dcsns in liked_discussions:
        if dcsns==d:
            show=None
            break
    for discuss in discuss_list:
        show_discuss[discuss.id]="yes"
        for dscs in liked_discusses:
            if dscs==discuss:
                show_discuss[discuss.id]=None
                break
    ##print discuss_list
    ##print "\n"
    ##print show_discuss
    return render(request,'nblik/discussion.html',{'discuss_list':discuss_list,'up':up,'discussion':d,'show':show,'show_discuss':show_discuss})

def discuss(request):
    if request.method=="GET":
        #print "Hello"
        discussion_id=request.GET["discussion_id"]
        #print discussion_id
        up_id=request.GET["user_id"]
        #print up_id
        discuss_text=request.GET["discuss_text"]
        dn=Discussion.objects.get(id=int(discussion_id))
        #print dn
        up=UserProfile.objects.get(id=int(up_id))
        #print up
        d=Discuss.objects.get_or_create(discuss_text=discuss_text,discuss_by=up,discuss_on=dn,likes=0)
        return HttpResponse(0)

def next_step(request):
    u=request.user
    if request.method=="POST":
        up=UserProfile.objects.get(user=u)
        name = request.POST.get('name')
        email = request.POST.get('email')
        dob_date = request.POST.get('dob_date')
        dob_month = request.POST.get('dob_month')
        dob_year = request.POST.get('dob_year')
        who=request.POST.get('who')
        lives_in=request.POST.get('lives_in')
        from_place=request.POST.get('from_place')
        if len(request.FILES) != 0:
            context_dict1 = cloudinary.uploader.upload(request.FILES['picture'],public_id = 'profile_pic/'+str(user),width = 400, height = 400, crop = 'fill',gravity = 'faces')
            userpro.picture = str(context_dict1['url'])
            ##print profile_pic_url
        languages=request.POST.get('language')
        profile_tagline=request.POST.get('profile_tag')
        liked_category_ids=request.POST.getlist('category')
        for i in liked_category_ids:
            cat=Category.objects.get(id=int(i))
            up.liked_categories.add(cat)
        up.name=name
        up.who=who
        up.lives_in=lives_in
        up.from_place=from_place
        try:
            up.dob_date=int(dob_date)
            up.dob_month=int(dob_month)
            up.dob_year=int(dob_year)
            up.languages=int(languages)
        except:
            pass 
        up.profile_tag_line=profile_tagline
        up.save()
        return HttpResponseRedirect('/nblik/')
    else:
        #try:
           # up=UserProfile.objects.get(user=u)
           # return HttpResponseRedirect('/nblik/')
        #except:
        context_dict={}
        cat_list=Category.objects.all()
        context_dict['cat_list']=cat_list
        return render(request,'nblik/next_step.html',context_dict)
            
def quick_add_blog(request):
    if request.method=="POST":
        blog_text=request.POST.get('quick_blog_text')
        form=BlogForm()
        context_dict={}
        context_dict['category_list'] = Category.objects.all()
        context_dict['quick_blog_text']= (str(blog_text)).replace("\r\n","<br />")
        #print blog_text
        context_dict['category']= None
        context_dict['myform']=form
        context_dict['blog_list']=Blog.objects.all()
        return render(request,'nblik/add_blog2.html',context_dict)

def post_to_facebook(request,blog_id):
    blog=Blog.objects.get(id=blog_id)
    user = request.user
    auth = user.social_auth.first()
    graph = facebook.GraphAPI(auth.extra_data['access_token'])
    graph.put_object('me', 'feed', message=blog.text)
    return HttpResponseRedirect('/nblik/')

def post_to_facebook_discussion(request,discussion_id):
    discussion=Discussion.objects.get(id=discussion_id)
    user = request.user
    auth = user.social_auth.first()
    graph = facebook.GraphAPI(auth.extra_data['access_token'])
    graph.put_object('me', 'feed', message=discussion.topic)
    return HttpResponseRedirect('/nblik/')


def blog_title(request):
    title=slugify(unidecode(request.GET['blog_title']))
    blogs=Blog.objects.all()
    resp="good"
    for blog in blogs:
        if blog.slug==title:
            resp="error"
            break
    return HttpResponse(resp)

def discussion_topic(request):
    title=slugify(unidecode(request.GET['discussion_topic']))
    discussions=Discussion.objects.all()
    resp="good"
    for disc in discussions:
        if disc.slug == title:
            resp="error"
            break
    return HttpResponse(resp)

def edit_language(request):
    user=request.user
    language=request.GET["language"]
    u=UserProfile.objects.get(user=user)
    u.languages=int(language)
    u.save()
    return HttpResponse('Done')

def edit_blog(request,blog_slug):
    blog=Blog.objects.get(slug=blog_slug)
    context_dict={}
    context_dict['blog_text']=(blog.blog_content).replace("\r\n","")
    context_dict['blog_title']=(blog.title)
    context_dict['blog_category']=str(blog.category.slug)
    context_dict['category_list']=Category.objects.all()
    form=BlogForm()
    context_dict['myform']=form
    context_dict['blog_id']=str(blog.id)
    return render(request,'nblik/edit_blog.html',context_dict)

def update_blog(request,category_name_slug):
    try:
        cat=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat=None

    if request.method=="POST":
        blog_f=BlogForm(request.POST)
        if blog_f.is_valid():
            title = blog_f.cleaned_data['title']
            blog_content=blog_f.cleaned_data['blog_content']
            blog_id=request.POST.get('blog_id')
            blog1=Blog.objects.get(id=int(blog_id))
            blog1.title=title
            blog1.blog_content=blog_content
            blog1.datetime_added=datetime.now()
            blog1.category=cat
            blog1.written_by=request.user
            blog1.save()
            modify_content(blog1.id)
            return blog(request,blog1.slug)
        else:
            blog1=Blog.objects.get(id=int(request.POST.get('blog_id')))
            blog_slug=blog1.slug
            return edit_blog(request,blog_slug)

def delete_blog(request,blog_slug):
    blog=Blog.objects.get(slug=blog_slug)
    blog.delete()
    return HttpResponseRedirect('/nblik/')

def edit_profile(request):
    user=request.user
    userpro=UserProfile.objects.get(user=user)
    context_dict={}
    context_dict['userpro']=userpro
    context_dict['name']=str(userpro.name)
    context_dict['tag']=str(userpro.profile_tag_line)
    context_dict['language']=str(userpro.languages)
    context_dict['date']=str(userpro.dob_date)
    context_dict['month']=str(userpro.dob_month)
    context_dict['year']=str(userpro.dob_year)
    context_dict['pic']=str(userpro.picture)
    return render(request,'nblik/edit_profile.html',context_dict)

def update_profile(request):
    user=request.user
    userpro=UserProfile.objects.get(user=user)
    userpro.name=request.POST.get('name')
    try:
        userpro.dob_date=int(request.POST.get('dob_date'))
        userpro.dob_month=int(request.POST.get('dob_month'))
        userpro.dob_year=int(request.POST.get('dob_year'))
        userpro.languages=int(request.POST.get('language'))
    except:
        pass
    userpro.profile_tag_line=request.POST.get('profile_tag')
    userpro.who=request.POST.get('who')
    userpro.lives_in=request.POST.get('lives_in')
    userpro.from_place=request.POST.get('from_place')
    if len(request.FILES) != 0:
        context_dict1 = cloudinary.uploader.upload(request.FILES['picture'],public_id='profile_pic/'+str(user),width = 400, height = 400, crop = 'fill',gravity='faces')
        userpro.picture = str(context_dict1['url'])
        ##print profile_pic_url
    userpro.save()
    return HttpResponseRedirect('/'+str(user)+'/')

def nblik_info(request,nblik_slug):
    nblik_o=NblikInfo.objects.get(slug=nblik_slug)
    return render(request,'nblik/nblik_info.html',{'nblik_o':nblik_o})

def edit_discussion(request,discussion_slug):
    discussion=Discussion.objects.get(slug=discussion_slug)
    context_dict={}
    context_dict['discussion']=discussion
    context_dict['discussion_intro']=(discussion.intro).replace("<br />","\r\n").replace("<br>","\r\n")
    context_dict['discussion_topic']=(discussion.topic)
    context_dict['discussion_category']=discussion.category
    context_dict['category_list']=Category.objects.all()
    context_dict['discussion_id']=str(discussion.id)
    #print discussion.category.slug
    return render(request,'nblik/edit_discussion.html',context_dict)

def delete_discussion(request,discussion_slug):
    discussion1=Discussion.objects.get(slug=discussion_slug)
    discussion1.delete()
    return HttpResponseRedirect('/nblik/')

def update_discussion(request):
    if request.method=="POST":
        topic = request.POST.get('discuss_topic')
        intro = request.POST.get('discuss_intro')
        cat=request.POST.get('category')
        d_id=request.POST.get('discussion_id')
        discussion1=Discussion.objects.get(id=int(d_id))
        discussion1.topic=topic
        discussion1.intro=intro.replace("\r\n","<br />").replace("\r","<br />").replace("\n","<br />")
        discussion1.category=Category.objects.get(slug=cat)
        discussion1.save()
        return discussion(request,discussion1.slug)

def unlike_blog(request):
    ##print "Hello"
    if request.method=="GET":
        blog_id=request.GET["blog_id"]
        blog=Blog.objects.get(id=int(blog_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        for blg in user2.liked_blogs.all():
            if blg==blog:
                user2.liked_blogs.remove(blog)
                user2.save()
                blog.likes-=1
                blog.save()
        return HttpResponse(blog.likes)

def unlike_discussion(request):
    ##print "Hello"
    if request.method=="GET":
        discussion_id=request.GET["discussion_id"]
        discussion=Discussion.objects.get(id=int(discussion_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        for dis in user2.liked_discussions.all():
            if dis==discussion:
                user2.liked_discussions.remove(discussion)
                user2.save()
                discussion.likes-=1
                discussion.save()
        return HttpResponse(discussion.likes)

def unlike_comment(request):
    ##print "Hello"
    if request.method=="GET":
        comment_id=request.GET["comment_id"]
        comment=Comment.objects.get(id=int(comment_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        for comm in user2.liked_comments.all():
            if comm==comment:
                user2.liked_comments.remove(comment)
                user2.save()
                comment.likes-=1
                comment.save()
        return HttpResponse(comment.likes)

def unlike_discuss(request):
    ##print "Hello"
    if request.method=="GET":
        discuss_id=request.GET["discuss_id"]
        discuss=Discuss.objects.get(id=int(discuss_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        for dis in user2.liked_discusses.all():
            if discuss==dis:
                user2.liked_discusses.remove(discuss)
                user2.save()
                discuss.likes-=1
                discuss.save()
        return HttpResponse(discuss.likes)

def unlike_category(request):
    if request.method=="GET":
        category_id=request.GET["category_id"]
        category1=Category.objects.get(id=int(category_id))
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        for cat in user2.liked_categories.all():
            if category1==cat:
                user2.liked_categories.remove(category1)
                user2.save()
                category1.likes-=1
                category1.save()
                break
        return HttpResponse(category1.likes)

def unfollow_user(request):
    if request.method=="GET":
        user_id=request.GET["user_id"]
        u=User.objects.get(id=int(user_id))
        userprofile=UserProfile.objects.get(user=u)
        ##print u
        up_follow=Follow.objects.get(userprofile=u)
        ##print up_follow
        up_follow.followers=up_follow.followers-1
        ##print up_follow.followers
        current_up_follow=Follow.objects.get(userprofile=request.user)
        ##print current_up_follow
        current_up_follow.followed.remove(userprofile)
        #print current_up_follow.no_followed
        current_up_follow.no_followed=current_up_follow.no_followed-1
        #print current_up_follow.no_followed
        ##print current_up_follow.no_followed
        current_up_follow.save()
        up_follow.save()
        ##print request.user
        return HttpResponse(current_up_follow.no_followed)