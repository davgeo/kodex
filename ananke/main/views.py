from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from .models import Server

import main.kodi as KodiLookUp

from operator import itemgetter

import logging
import threading

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
    server_down = True

    try:
      context['playing']    = KodiLookUp.Player_GetItem(*server)
      context['player']     = KodiLookUp.Player_GetProperties(*server)
      context['playlist']   = KodiLookUp.Playlist_GetItems(*server, playlistType='video')
      context['properties'] = KodiLookUp.Application_GetProperties(*server)
    except Exception as e:
      logging.info(e)
    else:
      server_down = False
      context['special_play'] = False

      try:
        playing_id = context['playing']['id']
      except KeyError:
        pass
      else:
        playlist_id_list = [item['id'] for item in context['playlist']]
        if playing_id not in playlist_id_list:
          context['special_play'] = True

    return func(request, server, context, server_down, *args, **kwargs)
  return wrapper

def ServerDownRedirect(func):
  def wrapper(request, server, context, server_down, *args, **kwargs):
    if server_down:
      return kodi(request)
    else:
      return func(request, server, context, *args, **kwargs)
  return wrapper

def ServerDownNoRedirect(func):
  def wrapper(request, server, context, server_down, *args, **kwargs):
    if server_down:
      return HttpResponse(status=503)
    else:
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
  def ThreadWrapper(result, index, func, *args, **kwargs):
    result[index] = func(*args, **kwargs)

  statusList = ['X']*len(context['kodi_servers'])
  activeThreads = []
  for i, server in enumerate(context['kodi_servers']):
    args = [statusList, i, KodiLookUp.Status] + list(server.conn())
    t = threading.Thread(target=ThreadWrapper, args=args)
    t.start()
    activeThreads.append(t)

  for thread in activeThreads:
    thread.join()

  context['kodi_server_list'] = [(s, statusList[i]) for i, s in enumerate(context['kodi_servers'])]
  return render(request, 'main/kodi_index.html', context)

@GetPlaylist
@ServerDownRedirect
def server(request, server, context):
  context['recentepisodes'] = KodiLookUp.VideoLibrary_GetRecentlyAddedEpisodes(*server)
  context['recentmovies'] = KodiLookUp.VideoLibrary_GetRecentlyAddedMovies(*server)
  return render(request, 'main/kodi_server_index.html', context)

@GetPlaylist
@ServerDownRedirect
def tvindex(request, server, context):
  unsorted_tvshow = KodiLookUp.VideoLibrary_GetTVShows(*server)
  context['tvshows'] = sorted(unsorted_tvshow, key=itemgetter('title'))
  return render(request, 'main/kodi_server_tv.html', context)

@GetPlaylist
@ServerDownRedirect
def tvshow(request, server, context, show_id):
  context['tvshow'] = KodiLookUp.VideoLibrary_GetTVShowDetails(*server, show_id=show_id)
  context['seasons'] = KodiLookUp.VideoLibrary_GetSeasons(*server, show_id=show_id)
  return render(request, 'main/kodi_server_tv_show.html', context)

@GetPlaylist
@ServerDownRedirect
def tvseason(request, server, context, show_id, season_id):
  context['tvshow'] = KodiLookUp.VideoLibrary_GetTVShowDetails(*server, show_id=show_id)
  context['season'] = season_id
  unsorted_episode_list = KodiLookUp.VideoLibrary_GetEpisodes(*server, show_id=show_id, season_id=season_id)
  context['episodes'] = sorted(unsorted_episode_list, key=itemgetter('episode'))
  return render(request, 'main/kodi_server_tv_season.html', context)

@GetPlaylist
@ServerDownRedirect
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
@ServerDownRedirect
def movies_index(request, server, context):
  unsorted_movie_list = KodiLookUp.VideoLibrary_GetMovies(*server)
  context['movies'] = sorted(unsorted_movie_list, key=itemgetter('title'))
  return render(request, 'main/kodi_server_movies.html', context)

@GetPlaylist
@ServerDownRedirect
def movie(request, server, context, movie_id):
  unsorted_movie_list = KodiLookUp.VideoLibrary_GetMovies(*server)

  for movie in unsorted_movie_list:
    if int(movie['movieid']) == int(movie_id):
      active_movie = movie

  movie_list = sorted(unsorted_movie_list, key=itemgetter('title'))

  context.update({'activemovie': active_movie,
                  'movies'     : movie_list})

  return render(request, 'main/kodi_server_movies.html', context)

@GetPlaylist
@ServerDownNoRedirect
def getplaylist(request, server, context):
  return render(request, 'main/kodi_playlist_panel.html', context)

@GetServer
def playmovie(request, server, context, movie_id):
  KodiLookUp.Playlist_Clear(*server, playlistType='video')
  KodiLookUp.Playlist_Add(*server, playlistType='video', params={'item':{'movieid':int(movie_id)}})
  movieInfo = KodiLookUp.VideoLibrary_GetMovieDetails(*server, movie_id=movie_id)
  KodiLookUp.Player_Open(*server, playlistType='video')
  KodiLookUp.Player_Seek(*server, position=movieInfo['resume']['percentage'])
  #KodiLookUp.Player_Open(*server, params={'item':{'movieid':int(movie_id)}, "options" : {"resume" : True}})
  return getplaylist(request, context['server'].id)

@GetServer
def addmovie(request, server, context, movie_id):
  KodiLookUp.Playlist_Add(*server, playlistType='video', params={'item':{'movieid':int(movie_id)}})
  return getplaylist(request, context['server'].id)

@GetServer
def playtv(request, server, context, show_id, season_id, episode_id):
  KodiLookUp.Playlist_Clear(*server, playlistType='video')
  KodiLookUp.Playlist_Add(*server, playlistType='video', params={'item':{'episodeid':int(episode_id)}})
  episodeInfo = KodiLookUp.VideoLibrary_GetEpisodeDetails(*server, episode_id=episode_id)
  KodiLookUp.Player_Open(*server, playlistType='video')
  KodiLookUp.Player_Seek(*server, position=episodeInfo['resume']['percentage'])
  #KodiLookUp.Player_Open(*server, params={'item':{'episodeid':int(episode_id)}, "options" : {"resume" : True}})
  return getplaylist(request, context['server'].id)

@GetServer
def addtv(request, server, context, show_id, season_id, episode_id):
  KodiLookUp.Playlist_Add(*server, playlistType='video', params={'item':{'episodeid':int(episode_id)}})
  return getplaylist(request, context['server'].id)

@GetServer
def watchedtv(request, server, context, show_id, season_id, episode_id):
  url = request.get_full_path().replace('_watched', '')
  episodeInfo = KodiLookUp.VideoLibrary_GetEpisodeDetails(*server, episode_id=episode_id)

  if episodeInfo['playcount'] > 0:
    playcount = 0
  else:
    playcount = 1

  KodiLookUp.VideoLibrary_SetEpisodeDetails(*server, episode_id=episode_id, playcount=playcount)
  return HttpResponse(status=200)

@GetServer
def removetvepisode(request, server, context, show_id, season_id, episode_id):
  url = request.get_full_path().replace('/{}_remove'.format(episode_id), '')
  KodiLookUp.VideoLibrary_RemoveEpisode(*server, episode_id=episode_id)
  return redirect(url)

@GetServer
def removetvshow(request, server, context, show_id):
  url = request.get_full_path().replace('/{}_remove'.format(show_id), '')
  KodiLookUp.VideoLibrary_RemoveTVShow(*server, show_id=show_id)
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
  KodiLookUp.Player_PlayPause(*server)
  return HttpResponse(status=200)

@GetServer
def stop(request, server, context):
  KodiLookUp.Player_Stop(*server)
  return getplaylist(request, context['server'].id)

@GetServer
def forward(request, server, context):
  KodiLookUp.Player_SetSpeed(*server, speed='increment')
  return HttpResponse(status=200)

@GetServer
def backward(request, server, context):
  KodiLookUp.Player_SetSpeed(*server, speed='decrement')
  return HttpResponse(status=200)

@GetServer
def skip(request, server, context):
  # goto next item in playlist ?
  KodiLookUp.Player_Seek(*server, position=100)
  return getplaylist(request, context['server'].id)

@GetServer
def restart(request, server, context):
  # get current position
  # if 0 Player.GoTo previous item in playlist
  KodiLookUp.Player_Seek(*server, position=0)
  return HttpResponse(status=200)

@GetServer
def mute(request, server, context):
  KodiLookUp.Application_SetMute(*server)
  return HttpResponse(status=200)

@GetServer
def togglesubtitles(request, server, context):
  properties = KodiLookUp.Player_GetProperties(*server)
  if properties['subtitleenabled']:
    mode = 'off'
  else:
    mode = 'on'
  KodiLookUp.Player_SetSubtitle(*server, mode=mode)
  return HttpResponse(status=200)

@GetServer
def cyclesubtitles(request, server, context):
  mode = 'next'
  KodiLookUp.Player_SetSubtitle(*server, mode=mode)
  return HttpResponse(status=200)

@GetServer
def remove(request, server, context, index):
  KodiLookUp.Playlist_Remove(*server, playlistType='video', index=index)
  return getplaylist(request, context['server'].id)

@GetServer
def playlistplay(request, server, context, index):
  KodiLookUp.Player_GoTo(*server, index=index)
  return getplaylist(request, context['server'].id)

@GetServer
def clear(request, server, context):
  KodiLookUp.Playlist_Clear(*server,  playlistType='video')
  return getplaylist(request, context['server'].id)

@GetServer
def videoscan(request, server, context):
  KodiLookUp.VideoLibrary_Scan(*server, show_dialog=True)
  return HttpResponse(status=200)

@GetServer
def quit(request, server, context):
  KodiLookUp.System_Shutdown(*server)
  return HttpResponseRedirect(reverse('kodi'))

@GetServer
def setvolume(request, server, context, volume):
  KodiLookUp.Application_SetVolume(*server, volume=volume)
  return HttpResponse(status=200)

@GetServer
def setprogress(request, server, context, percentage):
  KodiLookUp.Player_Seek(*server, position=percentage)
  return HttpResponse(status=200)

@GetServer
def getstatus(request, server, context):
  player_properties = KodiLookUp.Player_GetProperties(*server)
  application_properties = KodiLookUp.Application_GetProperties(*server)

  data = {}

  try:
    data['percentage'] = player_properties['percentage']
    data['speed'] = player_properties['speed']
  except KeyError:
    data['percentage'] = 0
    data['speed'] = 0

  data['volume'] = application_properties['volume']
  data['muted'] = application_properties['muted']
  return JsonResponse(data)
