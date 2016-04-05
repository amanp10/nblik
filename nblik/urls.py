from django.conf.urls import patterns, url
from nblik import views

urlpatterns = patterns('',
        url(r'^$',views.index,name='index'),
        url(r'^profile/$',views.profile,name="profile"),
        url(r'^password_reset_error/$',views.password_reset_error,name="password_reset_error"),
        url(r'^viewed/$',views.viewed,name="viewed"),
        url(r'^unlike_blog/$',views.unlike_blog,name="unlike_blog"),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.category,name ="category"),
        url(r'^(?P<username>[\w\-]+)/change_email/$',views.change_email,name ="change_email"),
        url(r'^blog/(?P<blog_title_slug>[\w\-]+)/$',views.blog,name="blog"),
        url(r'^like_category/$',views.like_category,name="like_category"),
        url(r'^unlike_category/$',views.unlike_category,name="unlike_category"),
        url(r'^like_discussion/$',views.like_discussion,name="like_discussion"),
        url(r'^unlike_discussion/$',views.unlike_discussion,name="unlike_discussion"),
        url(r'^like_discuss/$',views.like_discuss,name="like_discuss"),
        url(r'^unlike_discuss/$',views.unlike_discuss,name="unlike_discuss"),
        url(r'^like_comment/$',views.like_comment,name="like_comment"),
        url(r'^unlike_comment/$',views.unlike_comment,name="unlike_comment"),
        url(r'^suggest_category/$',views.suggest_category,name="suggest_category"),
        url(r'^like_blog/$',views.like_blog,name="like_blog"),
        url(r'^(?P<category_name_slug>[\w\-]+)/add_blog/$',views.add_blog2,name="add_blog"),
        url(r'^(?P<category_name_slug>[\w\-]+)/update_blog/$',views.update_blog,name="update_blog"),
        url(r'^update_discussion/$',views.update_discussion,name="update_discussion"),
        url(r'^update_profile/$',views.update_profile,name="update_profile"),
        url(r'^login_signup/',views.login_and_signup,name='login_signup'),
        url(r'^search_top/$',views.search_top,name='search_top'),
        url(r'^blog_title/$',views.blog_title,name='blog_title'),
        url(r'^discussion_topic/$',views.discussion_topic,name='discussion_topic'),
        url(r'^logout/$',views.user_logout,name='logout'),
        url(r'^google_login/$',views.google_login,name='google_login'),
        url(r'^follow_user/$',views.follow_user,name="follow_user"),
        url(r'^unfollow_user/$',views.unfollow_user,name="unfollow_user"),
        url(r'^comment/$',views.comment,name='comment'),
        url(r'^discuss/$',views.discuss,name='discuss'),
        url(r'^discussions/$',views.discussions,name='discussions'),
        url(r'^new_discussion/$',views.new_discussion,name='new_discussion'),
        url(r'^discussion/(?P<discussion_slug>[\w\-]+)/$',views.discussion,name="discussion"),
        url(r'^discussion_cat/(?P<category_slug>[\w\-]+)/$',views.discussion_2,name="discussion_2"),
        url(r'^info/(?P<nblik_slug>[\w\-]+)/',views.nblik_info,name="nblik_info"),
        url(r'^edit_blog/(?P<blog_slug>[\w\-]+)/$',views.edit_blog,name="edit_blog"),
        url(r'^edit_discussion/(?P<discussion_slug>[\w\-]+)/$',views.edit_discussion,name="edit_discussion"),
        url(r'^edit_profile/$',views.edit_profile,name="edit_profile"),
        url(r'^delete_blog/(?P<blog_slug>[\w\-]+)/$',views.delete_blog,name="delete_blog"),
        url(r'^delete_discussion/(?P<discussion_slug>[\w\-]+)/$',views.delete_discussion,name="delete_discussion"),
        url(r'^next_step/$',views.next_step,name="next_step"),
        url(r'^edit_language/$',views.edit_language,name="edit_language"),
        url(r'^quick_add_blog/$',views.quick_add_blog,name="quick_add_blog"),
        url(r'^reset_password/$',views.reset_password,name="reset_password"),
        url(r'^post_to_facebook/(?P<blog_id>[\w\-]+)/$',views.post_to_facebook,name="post_to_facebook"),
	url(r'^post_to_facebook_discussion/(?P<discussion_id>[\w\-]+)/$',views.post_to_facebook_discussion,name="post_to_facebook_discussion"),
        )
