from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from .models import Server, StarredTV, StarredMovie

import kodidj.kodi as KodiLookUp

from operator import itemgetter

import re
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
# Database Functions
#################################################
def AddServer(name, host, port, user, pwd):
  servers = Server.objects.create(name=name, host=host, port=port, user=user, pwd=pwd)
  servers.save()

def RemoveServer(server_id):
  db_entry = Server.objects.get(id=server_id)
  db_entry.delete()

def AddStarredTV(show_id):
  starredtvdb = StarredTV.objects.create(starred_id=show_id)
  starredtvdb.save()

def AddStarredMovie(movie_id):
  starredmoviedb = StarredMovie.objects.create(starred_id=movie_id)
  starredmoviedb.save()

def RemoveStarredTV(show_id):
  db_entry = StarredTV.objects.get(starred_id=show_id)
  db_entry.delete()

def RemoveStarredMovie(movie_id):
  db_entry = StarredMovie.objects.get(starred_id=movie_id)
  db_entry.delete()

def GetStarredTV():
  starred_tvshow_db_list = StarredTV.objects.all()
  starred_tvshow_id_list = [tvshow.get_id() for tvshow in starred_tvshow_db_list]
  return starred_tvshow_id_list

def GetStarredMovie():
  starred_movie_db_list = StarredMovie.objects.all()
  starred_movie_id_list = [movie.get_id() for movie in starred_movie_db_list]
  return starred_movie_id_list

#################################################
# Other Functions
#################################################
def GetMovieList(server, context, movie_id=None):
  unsorted_movie_list = KodiLookUp.VideoLibrary_GetMovies(*server)

  starred_movie_id_list = GetStarredMovie()

  starred_movie_list = []
  unstarred_movie_list = []

  for movie in unsorted_movie_list:
    if int(movie['movieid']) in starred_movie_id_list:
      movie['starred'] = True
      starred_movie_list.append(movie)
    else:
      movie['starred'] = False
      unstarred_movie_list.append(movie)

    if movie_id is not None:
      if int(movie['movieid']) == int(movie_id):
        context['activemovie'] = movie

  context['starred_movies'] = sorted(starred_movie_list, key=itemgetter('title'))
  context['movies'] = sorted(unstarred_movie_list, key=itemgetter('title'))

def GetTVShowList(server, context):
  unsorted_tvshow_list = KodiLookUp.VideoLibrary_GetTVShows(*server)

  starred_tv_id_list = GetStarredTV()

  starred_tv_list = []
  unstarred_tv_list = []

  for tvshow in unsorted_tvshow_list:
    if int(tvshow['tvshowid']) in starred_tv_id_list:
      tvshow['starred'] = True
      starred_tv_list.append(tvshow)
    else:
      tvshow['starred'] = False
      unstarred_tv_list.append(tvshow)

  context['starred_tvshows'] = sorted(starred_tv_list, key=itemgetter('title'))
  context['tvshows'] = sorted(unstarred_tv_list, key=itemgetter('title'))

#################################################
# Views
#################################################
@GetServerList
def index(request, context):
  return render(request, 'kodidj/index.html', context)

def kodi(request):
  return redirect(reverse('config'))

@GetServerList
def config(request, context):
  return render(request, 'kodidj/kodi_config.html', context)

@GetPlaylist
def setserver(request, server, context, server_down):
  if server_down:
    context = {}
  return render(request, 'kodidj/kodi_control_panel.html', context)

@GetServer
def pingserver(request, server, context):
  status = KodiLookUp.Status(*server)

  if status is 'Offline':
    return HttpResponse(status=500)
  else:
    return HttpResponse(status=200)

def addserver(request):
  try:
    server_name = request.POST['server_name']
    server_host = request.POST['server_host']
    server_port = request.POST['server_port']
    server_username = request.POST['server_username']
    server_password = request.POST['server_password']
  except KeyError:
    pass
  else:
    AddServer(server_name,server_host,server_port,server_username,server_password)
  return redirect(reverse('config'))

def removeserver(request):
  try:
    server_id = request.POST['server_id']
  except KeyError:
    pass
  else:
    RemoveServer(server_id)
  return redirect(reverse('config'))

@GetPlaylist
@ServerDownRedirect
def server(request, server, context):
  GetMovieList(server, context)
  GetTVShowList(server, context)
  context['recentepisodes'] = KodiLookUp.VideoLibrary_GetRecentlyAddedEpisodes(*server)
  context['recentmovies'] = KodiLookUp.VideoLibrary_GetRecentlyAddedMovies(*server)
  return render(request, 'kodidj/kodi_server_index.html', context)

@GetPlaylist
@ServerDownRedirect
def tvindex(request, server, context):
  GetTVShowList(server, context)
  return render(request, 'kodidj/kodi_server_tv.html', context)

@GetPlaylist
@ServerDownRedirect
def tvshow(request, server, context, show_id):
  context['tvshow'] = KodiLookUp.VideoLibrary_GetTVShowDetails(*server, show_id=show_id)
  context['seasons'] = KodiLookUp.VideoLibrary_GetSeasons(*server, show_id=show_id)
  return render(request, 'kodidj/kodi_server_tv_show.html', context)

@GetPlaylist
@ServerDownRedirect
def tvseason(request, server, context, show_id, season_id):
  context['tvshow'] = KodiLookUp.VideoLibrary_GetTVShowDetails(*server, show_id=show_id)
  context['season'] = season_id
  unsorted_episode_list = KodiLookUp.VideoLibrary_GetEpisodes(*server, show_id=show_id, season_id=season_id)
  context['episodes'] = sorted(unsorted_episode_list, key=itemgetter('episode'))
  return render(request, 'kodidj/kodi_server_tv_season.html', context)

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

  return render(request, 'kodidj/kodi_server_tv_season.html', context)

@GetPlaylist
@ServerDownRedirect
def movies_index(request, server, context):
  GetMovieList(server, context)
  return render(request, 'kodidj/kodi_server_movies.html', context)

@GetPlaylist
@ServerDownRedirect
def movie(request, server, context, movie_id):
  GetMovieList(server, context, movie_id)
  return render(request, 'kodidj/kodi_server_movies.html', context)

@GetPlaylist
@ServerDownNoRedirect
def getplaylist(request, server, context):
  return render(request, 'kodidj/kodi_playlist_panel.html', context)

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
def watchedmovie(request, server, context, movie_id):
  url = request.get_full_path().replace('_watched', '')
  movieInfo = KodiLookUp.VideoLibrary_GetMovieDetails(*server, movie_id=movie_id)

  if movieInfo['playcount'] > 0:
    playcount = 0
  else:
    playcount = 1

  KodiLookUp.VideoLibrary_SetMovieDetails(*server, movie_id=movie_id, playcount=playcount)
  return HttpResponse(status=200)

@GetServer
def starredmovie(request, server, context, movie_id):
  url = request.get_full_path().replace('/{}_starred'.format(movie_id), '')

  starred_movie_id_list = GetStarredMovie()

  if int(movie_id) in starred_movie_id_list:
    RemoveStarredMovie(movie_id)
  else:
    AddStarredMovie(movie_id)

  return redirect(url)

@GetServer
def removemovie(request, server, context, movie_id):
  url = request.get_full_path().replace('/{}_remove'.format(movie_id), '')
  KodiLookUp.VideoLibrary_RemoveMovie(*server, movie_id=movie_id)
  return redirect(url)

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
def starredtvshow(request, server, context, show_id):
  url = request.get_full_path().replace('/{}_starred'.format(show_id), '')

  starred_tv_id_list = GetStarredTV()

  if int(show_id) in starred_tv_id_list:
    RemoveStarredTV(show_id)
  else:
    AddStarredTV(show_id)

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
def setvolume(request, server, context):
  try:
    volume = request.GET['volume']
  except:
    pass
  else:
    KodiLookUp.Application_SetVolume(*server, volume=volume)
  finally:
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
