from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^kodi$', views.kodi, name='kodi'),
    url(r'^kodi/([0-9]+)$', views.server, name='server'),
    url(r'^kodi/([0-9]+)/tv$', views.tvindex, name='tvindex'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)$', views.tvshow, name='tvshow'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)/([0-9]+)$', views.tvseason, name='tvseason'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)/([0-9]+)_watched$', views.watchedtvseason, name='watchedtvseason'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)$', views.tvepisode, name='tvepisode'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)_play$', views.playtv, name='playtv'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)_add$', views.addtv, name='addtv'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)_watched$', views.watchedtv, name='watchedtv'),
    url(r'^kodi/([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)_remove$', views.removetv, name='removetv'),
    url(r'^kodi/([0-9]+)/movies$', views.movies_index, name='movies_index'),
    url(r'^kodi/([0-9]+)/movies/([0-9]+)$', views.movie, name='movie'),
    url(r'^kodi/([0-9]+)/movies/([0-9]+)_play$', views.playmovie, name='playmovie'),
    url(r'^kodi/([0-9]+)/movies/([0-9]+)_add$', views.addmovie, name='addmovie'),
    url(r'^kodi/([0-9]+).*?_playpause$', views.playpause, name='playpause'),
    url(r'^kodi/([0-9]+).*?_stop$', views.stop, name='stop'),
    url(r'^kodi/([0-9]+).*?_forward$', views.forward, name='forward'),
    url(r'^kodi/([0-9]+).*?_backward$', views.backward, name='backward'),
    url(r'^kodi/([0-9]+).*?_skip$', views.skip, name='skip'),
    url(r'^kodi/([0-9]+).*?_restart$', views.restart, name='restart'),
    url(r'^kodi/([0-9]+).*?_mute$', views.mute, name='mute'),
    url(r'^kodi/([0-9]+).*?_subtitles$', views.subtitles, name='subtitles'),
    url(r'^kodi/([0-9]+).*?_remove_([0-9]+)$', views.remove, name='remove'),
    url(r'^kodi/([0-9]+).*?_playlistplay_([0-9]+)$', views.playlistplay, name='playlistplay'),
    url(r'^kodi/([0-9]+).*?_clear$', views.clear, name='clear'),
    url(r'^kodi/([0-9]+).*?_setvolume_([0-9]+)$', views.setvolume, name='setvolume'),
]