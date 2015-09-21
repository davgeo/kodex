from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^kodi$', views.kodi, name='kodi'),
    url(r'^kodi/([0-9]+)$', views.server, name='server'),
    url(r'^kodi/([0-9]+)/tv$', views.tv, name='tv'),
    url(r'^kodi/([0-9]+)/movies$', views.movies, name='movies'),
]