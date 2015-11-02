from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from blogu.models import Category,Blog,UserProfile,Comment,Follow,Discussion,Discuss,Tag
from blogu.forms import BlogForm
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

def index(request):
    if request.method=="POST":
        blog_text=request.POST.get('blog_text')
        return render(request,'blogu/add_blog.html',{'blog_text':blog_text})
    blog_list = Blog.objects.order_by('-likes')[:10]
    show=[True]*len(blog_list)
    try:
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        liked_blogs_list=user2.liked_blogs.all()
        #print len(blog_list)
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
    #print datetime.now()
    #print show
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
    response = render(request,'blogu/index.html',context_dict)
    return response

def profile(request):
	pass

def category(request,category_name_slug):

    context_dict = {}
    context_dict['result_list']=None
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name']=category.name
        blog_list = Blog.objects.filter(category=category).order_by('-likes')
        context_dict['category']=category
        context_dict['category_name_slug']=category.slug
        show=[True]*len(blog_list)
        try:
            user1=User.objects.get(username=request.user)
            user2=UserProfile.objects.get(user=user1)
            liked_blogs_list=user2.liked_blogs.all()
            #print len(blog_list)
            for i in range(0,len(blog_list)):
                for lb in liked_blogs_list:
                    if lb == blog_list[i]:
                        show[i]=False
                        break
                    else:
                        show[i]=True
        except:
            pass
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
        zipped_data=zip(blog_list,b_time,show)
        context_dict['zipped_data']=zipped_data
    except Category.DoesNotExist:
        context_dict['category_name']=category_name_slug

    return render(request,'blogu/category.html',context_dict)


def get_category_list(max_results=0,startswith=''):
    cat_list=[]
    if startswith=='':
        cat_list = Category.objects.all()
    elif startswith:
        #print "Hello"
        cat_list = Category.objects.filter(name__istartswith=startswith)
        #print cat_list1
    if max_results>0:
        if len(cat_list)>max_results:
            cat_list=cat_list[:max_results]
    return cat_list

def blog(request,blog_title_slug):
    b=None
    c=None
    b_time=None
    try:
        b=Blog.objects.get(slug=blog_title_slug)
        print b.blog_content
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
    #print type(b.text)
    up=UserProfile.objects.get(user=request.user)
    show=False
    for bl in up.liked_blogs.all():
        if(bl==b):
            show=True
            break;
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
    return render(request,'blogu/blog.html',{'blog':b,'comments':comments,'b_time':b_time,'show':show,'u':request.user,'up':up,'comments_number':comments_number})


@login_required
def like_category(request):
    if request.method=="GET":
        category_id=request.GET["category_id"]
        category1=Category.objects.get(id=int(category_id))
        category1.likes+=1
        category1.save()
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        user2.liked_categories.add(category1)
        user2.save()
        return HttpResponse(category1.likes)

def suggest_category(request):
    str=request.GET["query_string"]
    #print str
    result=get_category_list(100,str)
    cat_list=[]
    for name in result:
        cat=Category.objects.get(name=name)
        cat_list.append(cat)
    #print cat_list
    return render(request,'blogu/category_list.html',{'cats':cat_list})
    #return HttpResponse(cat_list)

@login_required
def like_blog(request):
    #print "Hello"
    if request.method=="GET":
        blog_id=request.GET["blog_id"]
        blog=Blog.objects.get(id=int(blog_id))
        blog.likes+=1
        blog.save()
        #print request.user
        user1=User.objects.get(username=request.user)
        user2=UserProfile.objects.get(user=user1)
        user2.liked_blogs.add(blog)
        user2.save()
        return HttpResponse(blog.likes)

def add_blog(request,category_name_slug):
    try:
        cat=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat=None

    if request.method=="POST":
        if cat:
            blog_content=request.POST['blog_content']
            blog_title=request.POST['blog_title']
            #print type(blog_content)
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
            return blog(request,slugify(blog1.title))
    else:
        context_dict={'category_list':Category.objects.all(),'category':cat}
        return render(request,'blogu/add_blog.html',context_dict)

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
            blog1.id=cat.id
            blog1.written_by=request.user
            blog1.save()
            return blog(request,slugify(blog1.title))
        else:
            print blog_form.errors
    else:
        form=BlogForm()
        context_dict={'category_list':Category.objects.all(),'category':cat,'myform':form}
        return render(request,'blogu/add_blog2.html',context_dict)

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
                    return HttpResponseRedirect('/blogu/')
                else:
                    return HttpResponse("Your Nblik account is disabled.")
            else:
                print "Invalid login details: {0}, {1}".format(login_username,login_password)
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
                    print user1
                    login(request,user1)
                    return render(request,'blogu/next_step.html',{'email':signup_email,'name':signup_name}) 
                    #return render(request,'blogu/signup2.html',{'username':signup_username})

        return render(request,'blogu/login.html',{'login_statement':login_statement,'signup_statement':signup_statement,'cat_list':Category.objects.all()})
    else:
        return render(request,'blogu/login.html',{})

def google_login(request):
    if request.method=="POST":
        #print "Hello"
        email=request.POST['email']
        image_url=request.POST['image_url']
        name=request.POST['name']
        google_id=request.POST['id']
        response_dict={}
        print "email=",email
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
                    #print "Hello"
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
            print "In except"
            signup_username=create_signup_username(name)
            print signup_username,email
            user=User.objects.create_user(username=signup_username,email=email)
            user.set_password("password")
            user.save()
            user1=User.objects.get(username=signup_username)
            print "user1=", user1
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
    str=request.GET["query_string"]
    #print str
    result=get_category_list(100,str)
    cat_list=[]
    for name in result:
        cat=Category.objects.get(name=name)
        cat_list.append(cat)

    blog_list=Blog.objects.all()
    b_list=[]
    for blog in blog_list:
        title=blog.title
        for word in title.split():
            if word.startswith(str):
                b_list.append(blog)
                break

    user_list = UserProfile.objects.all()
    u_list=[]
    for u in user_list:
        if u.name.startswith(str):
           u_list.append(u)
    #print cat_list,b_list,u_list
    #print cat_list
    context_dict={}
    context_dict['cats']=cat_list
    context_dict['blogs']=b_list
    context_dict['users']=u_list
    #print context_dict
    #return HttpResponse("Results")
    return render(request,"blogu/search_results.html", context_dict)

    #return HttpResponse(cat_list)

def user_logout(request):
    logout(request)
    print "Hello"
    return HttpResponseRedirect('/blogu/')


def follow_user(request):
    if request.method=="GET":
        user_id=request.GET["user_id"]
        userprofile=UserProfile.objects.get(id=int(user_id))
        u=User.objects.get(username=userprofile.user.username)
        #print u
        up_follow=Follow.objects.get(userprofile=u)
        up=UserProfile.objects.get(user=u)
        #print up_follow
        up_follow.followers=up_follow.followers+1
        #print up_follow.followers
        current_up_follow=Follow.objects.get(userprofile=request.user)
        #print current_up_follow
        current_up_follow.followed.add(up)
        current_up_follow.no_followed=current_up_follow.no_followed+1
        #print current_up_follow.no_followed
        current_up_follow.save()
        up_follow.save()
        #print request.user
        return HttpResponse("followed")


def dashboard(request,username):
    context_dict={}
    try:
        user=User.objects.get(username=username)
        userprofile=UserProfile.objects.get(user=user)
        userprofile_follow=Follow.objects.get(userprofile=user)
        followed_tags=userprofile.followed_tags.all()
        followed_list=userprofile_follow.followed.all()
        followers=userprofile.follow_set.all()
        #print followers
    except:
        user=None
        userprofile=None
        userprofile_follow=None
        followed_tags=None
        followed_list=None
        followers=None
    context_dict['user']=user
    context_dict['userprofile']=userprofile
    context_dict['userprofile_follow']=userprofile_follow
    context_dict['followed_tags']=followed_tags
    context_dict['followed_list']=followed_list
    context_dict['followers']=followers
    return render(request,'blogu/dashboard.html',context_dict)

def comment(request):
    if request.method=="GET":
        #print "Hello"
        blog_id=request.GET["blog_id"]
        #print blog_id
        user_id=request.GET["user_id"]
        #print user_id
        comment_text=request.GET["comment_text"]
        b=Blog.objects.get(id=int(blog_id))
        #print b
        u=User.objects.get(id=int(user_id))
        print b,u
        c=Comment.objects.get_or_create(comment_text=comment_text,comment_by=u,comment_to=b,likes=0)
        return HttpResponse(0)

def add_propic(request):
    return HttpResponse("hello")
    #return render(request,'blogu/add_propic.html',{})
    #return HttpResponse("hello")
    return render(request,"blogu/add_propic.html",{})

def discussions(request):
    discussions=Discussion.objects.all()
    return render(request,'blogu/discussions.html',{'discussions':discussions})

def new_discussion(request):
    pass

def discussion(request,discussion_slug):
    d=Discussion.objects.get(slug=discussion_slug)
    discuss_list=d.discuss_set.all()
    up=UserProfile.objects.get(user=request.user)
    print discuss_list
    return render(request,'blogu/discussion.html',{'discuss_list':discuss_list,'up':up,'discussion':d})

def discuss(request):
    if request.method=="GET":
        print "Hello"
        discussion_id=request.GET["discussion_id"]
        print discussion_id
        up_id=request.GET["user_id"]
        print up_id
        discuss_text=request.GET["discuss_text"]
        dn=Discussion.objects.get(id=int(discussion_id))
        print dn
        up=UserProfile.objects.get(id=int(up_id))
        print up
        d=Discuss.objects.get_or_create(discuss_text=discuss_text,discuss_by=up,discuss_on=dn,likes=0)
        return HttpResponse(0)

def next_step(request):
    u=request.user
    if request.method=="POST":
        up=UserProfile(user=u,level=1)
        name = request.POST.get('name')
        email = request.POST.get('email')
        dob_date = request.POST.get('dob_date')
        dob_month = request.POST.get('dob_month')
        dob_year = request.POST.get('dob_year')
        profile_pic_url=request.FILES['picture']
        print profile_pic_url
        languages=request.POST.get('languages')
        profile_tagline=request.POST.get('profile_tagline')
        liked_category_ids=request.POST.getlist('category')
        up.name=name
        up.dob_date=int(dob_date)
        up.dob_month=int(dob_month)
        up.dob_year=int(dob_year)
        up.languages=int(languages) 
        up.profile_tag_line=profile_tagline
        up.save()
        up_follow=Follow(userprofile=u)
        up_follow.save()
        return HttpResponseRedirect('/blogu/')
    else:
        try:
            up=UserProfile.objects.get(user=u)
            return HttpResponseRedirect('/blogu/')
        except:
            context_dict={}
            cat_list=Category.objects.all()
            context_dict['cat_list']=cat_list
            return render(request,'blogu/next_step.html',context_dict)
            
def quick_add_blog(request):
    if request.method=="POST":
        blog_text=request.POST.get('quick_blog_text')
        context_dict={}
        context_dict['category_list'] = Category.objects.all()
        context_dict['quick_blog_text']= blog_text
        context_dict['cat']= None
        return render(request,'blogu/add_blog.html',context_dict)

def post_to_facebook(request,blog_id):
    blog=Blog.objects.get(id=blog_id)
    user = request.user
    auth = user.social_auth.first()
    graph = facebook.GraphAPI(auth.extra_data['access_token'])
    graph.put_object('me', 'feed', message=blog.text)
    return HttpResponseRedirect('/blogu/')
