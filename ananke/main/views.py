from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

from .models import Server

import main.kodi as KodiLookUp

from operator import itemgetter

# Todo: Implement status lookin in parallel
#import threading
#from queue import Queue

#################################################
# Decorators
#################################################
def GetServerList(func):
  def wrapper(request, *args, **kwargs):
    serverList = Server.objects.all()
    context = {'kodi_servers': serverList}
    return func(request, context, *args, **kwargs)
  return wrapper

def GetServer(func):
  @GetServerList
  def wrapper(request, context, server_id, *args, **kwargs):
    server = Server.objects.get(pk=server_id)
    context['server'] = server
    return func(request, server.conn(), context, *args, **kwargs)
  return wrapper

def GetPlaylist(func):
  @GetServer
  def wrapper(request, server, context, *args, **kwargs):
    context['playing']  = KodiLookUp.Player_GetItem(*server)
    context['player']   = KodiLookUp.Player_GetProperties(*server)
    context['playlist'] = KodiLookUp.Playlist_GetItems(*server, playlistType='video')
    context['properties']   = KodiLookUp.Application_GetProperties(*server)
    return func(request, server, context, *args, **kwargs)
  return wrapper

#################################################
# Views
#################################################
@GetServerList
def index(request, context):
  return render(request, 'main/index.html', context)

@GetServerList
def kodi(request, context):
  serverList = Server.objects.all()

  serverStatusTable = []
  for server in serverList:
    serverStatusTable.append((server, KodiLookUp.Status(*server.conn())))

  context['kodi_server_list'] = serverStatusTable
  #context['path'] = 'kodi'
  return render(request, 'main/kodi_index.html', context)

@GetPlaylist
def server(request, server, context):
  context['recentepisodes'] = KodiLookUp.VideoLibrary_GetRecentlyAddedEpisodes(*server)
  context['recentmovies'] = KodiLookUp.VideoLibrary_GetRecentlyAddedMovies(*server)
  #context['path'] = 'kodi / {0}'.format(context['server'].name)
  return render(request, 'main/kodi_server_index.html', context)

@GetPlaylist
def tvindex(request, server, context):
  unsorted_tvshow = KodiLookUp.VideoLibrary_GetTVShows(*server)
  context['tvshows'] = sorted(unsorted_tvshow, key=itemgetter('title'))
  #context['path'] = 'kodi / {0} / tv'.format(context['server'].name)
  return render(request, 'main/kodi_server_tv.html', context)

@GetPlaylist
def tvshow(request, server, context, show_id):
  context['tvshow'] = KodiLookUp.VideoLibrary_GetTVShowDetails(*server, show_id=show_id)
  context['seasons'] = KodiLookUp.VideoLibrary_GetSeasons(*server, show_id=show_id)
  #context['path'] = 'kodi / {0} / tv / {1}'.format(context['server'].name, context['tvshow']['title'])
  return render(request, 'main/kodi_server_tv_show.html', context)

@GetPlaylist
def tvseason(request, server, context, show_id, season_id):
  context['tvshow'] = KodiLookUp.VideoLibrary_GetTVShowDetails(*server, show_id=show_id)
  context['season'] = season_id
  unsorted_episode_list = KodiLookUp.VideoLibrary_GetEpisodes(*server, show_id=show_id, season_id=season_id)
  context['episodes'] = sorted(unsorted_episode_list, key=itemgetter('episode'))
  #context['path'] = 'kodi / {0} / tv / {1} / {2}'.format(context['server'].name, context['tvshow']['title'], "Season {0}".format(season_id))
  return render(request, 'main/kodi_server_tv_season.html', context)

@GetPlaylist
def tvepisode(request, server, context, show_id, season_id, episode_id):
  context['tvshow'] = KodiLookUp.VideoLibrary_GetTVShowDetails(*server, show_id=show_id)
  context['season'] = season_id

  unsorted_episode_list = KodiLookUp.VideoLibrary_GetEpisodes(*server, show_id=show_id, season_id=season_id)

  episode_list = sorted(unsorted_episode_list, key=itemgetter('episode'))

  for episode in episode_list:
    if int(episode['episodeid']) == int(episode_id):
      active_episode = episode

  context.update({'activeepisode' : active_episode,
                  'episodes'      : episode_list})

  return render(request, 'main/kodi_server_tv_season.html', context)

@GetPlaylist
def movies_index(request, server, context):
  unsorted_movie_list = KodiLookUp.VideoLibrary_GetMovies(*server)
  context['movies'] = sorted(unsorted_movie_list, key=itemgetter('title'))
  return render(request, 'main/kodi_server_movies.html', context)

@GetPlaylist
def movie(request, server, context, movie_id):
  unsorted_movie_list = KodiLookUp.VideoLibrary_GetMovies(*server)

  for movie in unsorted_movie_list:
    if int(movie['movieid']) == int(movie_id):
      active_movie = movie

  movie_list = sorted(unsorted_movie_list, key=itemgetter('title'))

  context.update({'activemovie': active_movie,
                  'movies'     : movie_list})

  return render(request, 'main/kodi_server_movies.html', context)

@GetServer
def playmovie(request, server, context, movie_id):
  url = request.get_full_path().replace('_play', '')
  KodiLookUp.Playlist_Clear(*server, playlistType='video')
  KodiLookUp.Playlist_Add(*server, playlistType='video', params={'item':{'movieid':int(movie_id)}})
  movieInfo = KodiLookUp.VideoLibrary_GetMovieDetails(*server, movie_id=movie_id)
  KodiLookUp.Player_Open(*server, playlistType='video')
  KodiLookUp.Player_Seek(*server, position=movieInfo['resume']['percentage'])
  #KodiLookUp.Player_Open(*server, params={'item':{'movieid':int(movie_id)}, "options" : {"resume" : True}})
  return redirect(url)

@GetServer
def addmovie(request, server, context, movie_id):
  url = request.get_full_path().replace('_add', '')
  KodiLookUp.Playlist_Add(*server, playlistType='video', params={'item':{'movieid':int(movie_id)}})
  return redirect(url)

@GetServer
def playtv(request, server, context, show_id, season_id, episode_id):
  url = request.get_full_path().replace('_play', '')
  KodiLookUp.Playlist_Clear(*server, playlistType='video')
  KodiLookUp.Playlist_Add(*server, playlistType='video', params={'item':{'episodeid':int(episode_id)}})
  episodeInfo = KodiLookUp.VideoLibrary_GetEpisodeDetails(*server, episode_id=episode_id)
  KodiLookUp.Player_Open(*server, playlistType='video')
  KodiLookUp.Player_Seek(*server, position=episodeInfo['resume']['percentage'])
  #KodiLookUp.Player_Open(*server, params={'item':{'episodeid':int(episode_id)}, "options" : {"resume" : True}})
  return redirect(url)

@GetServer
def addtv(request, server, context, show_id, season_id, episode_id):
  url = request.get_full_path().replace('_add', '')
  KodiLookUp.Playlist_Add(*server, playlistType='video', params={'item':{'episodeid':int(episode_id)}})
  return redirect(url)

@GetServer
def watchedtv(request, server, context, show_id, season_id, episode_id):
  url = request.get_full_path().replace('_watched', '')
  episodeInfo = KodiLookUp.VideoLibrary_GetEpisodeDetails(*server, episode_id=episode_id)

  if episodeInfo['playcount'] > 0:
    playcount = 0
  else:
    playcount = 1

  KodiLookUp.VideoLibrary_SetEpisodeDetails(*server, episode_id=episode_id, playcount=playcount)
  return redirect(url)

@GetServer
def watchedtvseason(request, server, context, show_id, season_id):
  url = request.get_full_path().replace('/{}_watched'.format(season_id), '')

  seasons = KodiLookUp.VideoLibrary_GetSeasons(*server, show_id=show_id)

  for season in seasons:
    if int(season['season']) == int(season_id):
      active_season = season

  if active_season['playcount'] > 0:
    playcount = 0
  else:
    playcount = 1

  unsorted_episode_list = KodiLookUp.VideoLibrary_GetEpisodes(*server, show_id=show_id, season_id=season_id)
  episode_list = sorted(unsorted_episode_list, key=itemgetter('episode'))

  for episode in episode_list:
    KodiLookUp.VideoLibrary_SetEpisodeDetails(*server, episode_id=episode['episodeid'], playcount=playcount)

  return redirect(url)

@GetServer
def playpause(request, server, context):
  # Revisit this, doesn't play if stopped
  url = request.get_full_path().replace('_playpause', '')
  KodiLookUp.Player_PlayPause(*server)
  return redirect(url)

@GetServer
def stop(request, server, context):
  url = request.get_full_path().replace('_stop', '')
  KodiLookUp.Player_Stop(*server)
  return redirect(url)

@GetServer
def forward(request, server, context):
  url = request.get_full_path().replace('_forward', '')
  KodiLookUp.Player_SetSpeed(*server, speed='increment')
  return redirect(url)

@GetServer
def backward(request, server, context):
  url = request.get_full_path().replace('_backward', '')
  KodiLookUp.Player_SetSpeed(*server, speed='decrement')
  return redirect(url)

@GetServer
def skip(request, server, context):
  url = request.get_full_path().replace('_skip', '')
  # goto next item in playlist ?
  KodiLookUp.Player_Seek(*server, position=100)
  return redirect(url)

@GetServer
def restart(request, server, context):
  url = request.get_full_path().replace('_restart', '')
  # get current position
  # if 0 Player.GoTo previous item in playlist
  KodiLookUp.Player_Seek(*server, position=0)
  return redirect(url)

@GetServer
def mute(request, server, context):
  url = request.get_full_path().replace('_mute', '')
  KodiLookUp.Application_SetMute(*server)
  return redirect(url)

@GetServer
def subtitles(request, server, context):
  url = request.get_full_path().replace('_subtitles', '')
  KodiLookUp.Player_SetSubtitle(*server)
  return redirect(url)

@GetServer
def remove(request, server, context, index):
  url = request.get_full_path().replace('_remove_{0}'.format(index), '')
  KodiLookUp.Playlist_Remove(*server, playlistType='video', index=index)
  return redirect(url)

@GetServer
def playlistplay(request, server, context, index):
  url = request.get_full_path().replace('_playlistplay_{0}'.format(index), '')
  KodiLookUp.Player_GoTo(*server, index=index)
  return redirect(url)

@GetServer
def clear(request, server, context):
  url = request.get_full_path().replace('_clear', '')
  KodiLookUp.Playlist_Clear(*server,  playlistType='video')
  return redirect(url)

@GetServer
def setvolume(request, server, context, volume):
  KodiLookUp.Application_SetVolume(*server, volume=volume)
  return HttpResponse(status=200)

