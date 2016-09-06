from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.kodi, name='kodi'),
    url(r'^.*?_setserver_([0-9]+)$', views.setserver, name='setserver'),
    url(r'^addserver$', views.addserver, name='addserver'), # POST
    url(r'^removeserver$', views.removeserver, name='removeserver'), # POST
    url(r'^pingserver_([0-9]+)$', views.pingserver, name='pingserver'),
    url(r'^config$', views.config, name='config'),
    url(r'^([0-9]+)$', views.server, name='server'),
    url(r'^([0-9]+)/tv$', views.tvindex, name='tvindex'),
    url(r'^([0-9]+)/tv/([0-9]+)$', views.tvshow, name='tvshow'),
    url(r'^([0-9]+)/tv/([0-9]+)_remove$', views.removetvshow, name='removetvshow'),
    url(r'^([0-9]+)/tv/([0-9]+)_starred$', views.starredtvshow, name='starredtvshow'),
    url(r'^([0-9]+)/tv/([0-9]+)/([0-9]+)$', views.tvseason, name='tvseason'),
    url(r'^([0-9]+)/tv/([0-9]+)/([0-9]+)_watched$', views.watchedtvseason, name='watchedtvseason'),
    url(r'^([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)$', views.tvepisode, name='tvepisode'),
    url(r'^([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)_play$', views.playtv, name='playtv'),
    url(r'^([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)_add$', views.addtv, name='addtv'),
    url(r'^([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)_watched$', views.watchedtv, name='watchedtv'),
    url(r'^([0-9]+)/tv/([0-9]+)/([0-9]+)/([0-9]+)_remove$', views.removetvepisode, name='removetvepisode'),
    url(r'^([0-9]+)/movies$', views.movies_index, name='movies_index'),
    url(r'^([0-9]+)/movies/([0-9]+)$', views.movie, name='movie'),
    url(r'^([0-9]+)/movies/([0-9]+)_play$', views.playmovie, name='playmovie'),
    url(r'^([0-9]+)/movies/([0-9]+)_add$', views.addmovie, name='addmovie'),
    url(r'^([0-9]+)/movies/([0-9]+)_watched$', views.watchedmovie, name='watchedmovie'),
    url(r'^([0-9]+)/movies/([0-9]+)_starred', views.starredmovie, name='starredmovie'),
    url(r'^([0-9]+)/movies/([0-9]+)_remove$', views.removemovie, name='removemovie'),
    url(r'^([0-9]+).*?_playpause$', views.playpause, name='playpause'),
    url(r'^([0-9]+).*?_stop$', views.stop, name='stop'),
    url(r'^([0-9]+).*?_forward$', views.forward, name='forward'),
    url(r'^([0-9]+).*?_backward$', views.backward, name='backward'),
    url(r'^([0-9]+).*?_skip$', views.skip, name='skip'),
    url(r'^([0-9]+).*?_restart$', views.restart, name='restart'),
    url(r'^([0-9]+).*?_mute$', views.mute, name='mute'),
    url(r'^([0-9]+).*?_togglesubtitles$', views.togglesubtitles, name='togglesubtitles'),
    url(r'^([0-9]+).*?_cyclesubtitles$', views.cyclesubtitles, name='cyclesubtitles'),
    url(r'^([0-9]+).*?_remove_([0-9]+)$', views.remove, name='remove'),
    url(r'^([0-9]+).*?_playlistplay_([0-9]+)$', views.playlistplay, name='playlistplay'),
    url(r'^([0-9]+).*?_clear$', views.clear, name='clear'),
    url(r'^([0-9]+).*?_videoscan$', views.videoscan, name='videoscan'),
    url(r'^([0-9]+).*?_quit$', views.quit, name='quit'),
    url(r'^([0-9]+).*?_setvolume$', views.setvolume, name='setvolume'), # GET
    url(r'^([0-9]+).*?_setprogress_([0-9]+)$', views.setprogress, name='setprogress'),
    url(r'^([0-9]+).*?_getstatus$', views.getstatus, name='getstatus'),
    url(r'^([0-9]+).*?_getplaylist$', views.getplaylist, name='getplaylist'),
]