#from registration.backends.simple.views import RegistrationView
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from nblik import views
#class MyRegistrationView(RegistrationView):
#    def get_success_url(self,request,user):
#        return '/nblik/'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^nblik/', include('nblik.urls')),
	url(r'^$', views.welcome,name='welcome'),
	#url(r'^accounts/register/$', MyRegistrationView.as_view(),name = 'registration_register'),
	url(r'^accounts/',include('registration.backends.simple.urls')),
    url(r'^(?P<username>[\w\-]+)/$',views.dashboard,name='dashboard'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),
)
