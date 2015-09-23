#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from website import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ytdjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logoutuser/$', views.logoutuser, name='logoutuser'),
    url(r'^help/$', views.help, name='help'),
    url(r'^files/$', views.files, name='files'),
    url(ur'^delete_file/(?P<file>.*)$', views.delete_file, name='delete_file'),
    url(r'^files_queued/$', views.files_queued, name='files_queued'),
    url(r'^files_errors/$', views.files_errors, name='files_errors'),
    url(r'^files_converted/$', views.files_converted, name='files_converted'),
    url(r'^files_convert/$', views.files_convert, name='files_convert'),
    url(r'^user_profile/$', views.user_profile, name='user_profile'),

)
