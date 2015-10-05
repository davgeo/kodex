from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

from .models import Server

import main.kodi as KodiLookUp

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
    context['playlist'] = KodiLookUp.Playlist_GetItems(*server, playlistType='video')
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
  context['path'] = 'kodi'
  return render(request, 'main/kodi_index.html', context)

@GetPlaylist
def server(request, server, context):
  context['episodes'] = KodiLookUp.VideoLibrary_GetRecentlyAddedEpisodes(*server)
  context['movies'] = KodiLookUp.VideoLibrary_GetRecentlyAddedMovies(*server)
  context['path'] = 'kodi / {0}'.format(context['server'].name)
  return render(request, 'main/kodi_server_index.html', context)

@GetPlaylist
def tvindex(request, server, context):
  context['tvshows'] = KodiLookUp.VideoLibrary_GetTVShows(*server)
  context['path'] = 'kodi / {0} / tv'.format(context['server'].name)
  return render(request, 'main/kodi_server_tv.html', context)

@GetPlaylist
def tvshow(request, server, context, show_id):
  # get show details for ID (show title, thumbnail etc)
  context['seasons'] = KodiLookUp.VideoLibrary_GetSeasons(*server, show_id=show_id)
  #context['path'] = 'kodi / {0} / tv / {1}'.format(context['server'].name, show_id)
  return render(request, 'main/kodi_server_tv_show.html', context)

@GetPlaylist
def tvseason(request, server, context, show_id, season_id):
  context['episodes'] = KodiLookUp.VideoLibrary_GetEpisodes(*server, show_id=show_id, season_id=season_id)
  return render(request, 'main/kodi_server_tv_season.html', context)

@GetPlaylist
def tvepisode(request, server, context, show_id, season_id, episode_id):
  episode_list = KodiLookUp.VideoLibrary_GetEpisodes(*server, show_id=show_id, season_id=season_id)

  for episode in episode_list:
    if int(episode['episodeid']) == int(episode_id):
      name = episode['title']
      plot = episode['plot']

  context.update({'episodes'  : episode_list,
                  'subheading': name,
                  'subtext'   : plot})

  return render(request, 'main/kodi_server_tv_season.html', context)

@GetPlaylist
def movies_index(request, server, context):
  context['movies'] = KodiLookUp.VideoLibrary_GetMovies(*server)
  return render(request, 'main/kodi_server_movies.html', context)

@GetPlaylist
def movie(request, server, context, movie_id):
  movie_list = KodiLookUp.VideoLibrary_GetMovies(*server)

  for movie in movie_list:
    if int(movie['movieid']) == int(movie_id):
      name = movie['title']
      plot = movie['plot']

  context.update({'movies'    : movie_list,
                  'subheading': name,
                  'subtext'   : plot})

  return render(request, 'main/kodi_server_movies.html', context)

@GetServer
def playpause(request, server, context):
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