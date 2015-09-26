from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^kodi$', views.kodi, name='kodi'),
    url(r'^kodi/([0-9]+)$', views.server, name='server'),
    url(r'^kodi/([0-9]+)/tv$', views.tvindex, name='tvindex'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)$', views.tvshow, name='tvshow'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)/([0-9]+)$', views.tvseason, name='tvseason'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)$', views.tvseason, name='tvepisode'),
    url(r'^kodi/([0-9]+)/movies$', views.movies_index, name='movies_index'),
    url(r'^kodi/([0-9]+)/movies/([0-9]+)$', views.movie, name='movie')
]