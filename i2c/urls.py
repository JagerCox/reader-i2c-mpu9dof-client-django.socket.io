"""i2c URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import settings
import socketio.sdjango
from interface.views import *
from django.contrib import admin
from django.conf.urls import patterns, include, url

socketio.sdjango.autodiscover()

urlpatterns = patterns('',
    url("^socket\.io", include(socketio.sdjango.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url("^$", HomeView.as_view(), name="home"),
)

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    '''Production'''
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
else:
    '''Deployment'''
    urlpatterns += patterns('django.contrib.staticfiles.views',
       url(r'^static/(?P<path>.*)$', 'serve'),
    )
