from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from .models import Server, StarredTV, StarredMovie

import os
import re
import logging
import threading
from operator import itemgetter

import kodicontroller

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

def GetController(func):
  @GetServer
  def wrapper(request, server, context, *args, **kwargs):
    controller = kodicontroller.KodiController()
    controller.SetServer(*server)
    controller.SetThumbnailCache(os.path.join('static', 'cache'))
    return func(request, controller, context, *args, **kwargs)
  return wrapper

def GetPlaylist(func):
  @GetController
  def wrapper(request, controller, context, *args, **kwargs):
    server_down = True

    try:
      context['playing']    = controller.Player_GetItem()
      context['player']     = controller.Player_GetProperties()
      context['playlist']   = controller.Playlist_GetItems(playlistType='video')
      context['properties'] = controller.Application_GetProperties()
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

    return func(request, controller, context, server_down, *args, **kwargs)
  return wrapper

def ServerDownRedirect(func):
  def wrapper(request, controller, context, server_down, *args, **kwargs):
    if server_down:
      return kodi(request)
    else:
      return func(request, controller, context, *args, **kwargs)
  return wrapper

def ServerDownNoRedirect(func):
  def wrapper(request, controller, context, server_down, *args, **kwargs):
    if server_down:
      return HttpResponse(status=503)
    else:
      return func(request, controller, context, *args, **kwargs)
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
def GetMovieList(controller, context, movie_id=None):
  unsorted_movie_list = controller.VideoLibrary_GetMovies()

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

def GetTVShowList(controller, context):
  unsorted_tvshow_list = controller.VideoLibrary_GetTVShows()

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
def kodi(request):
  return redirect(reverse('config'))

@GetServerList
def config(request, context):
  return render(request, 'kodidj/kodi_config.html', context)

@GetPlaylist
def setserver(request, controller, context, server_down):
  if server_down:
    context = {}
  return render(request, 'kodidj/kodi_control_panel.html', context)

@GetController
def pingserver(request, controller, context):
  status = controller.Status()

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
def server(request, controller, context):
  GetMovieList(controller, context)
  GetTVShowList(controller, context)
  context['recentepisodes'] = controller.VideoLibrary_GetRecentlyAddedEpisodes()
  context['recentmovies'] = controller.VideoLibrary_GetRecentlyAddedMovies()
  return render(request, 'kodidj/kodi_server_index.html', context)

@GetPlaylist
@ServerDownRedirect
def tvindex(request, controller, context):
  GetTVShowList(controller, context)
  return render(request, 'kodidj/kodi_server_tv.html', context)

@GetPlaylist
@ServerDownRedirect
def tvshow(request, controller, context, show_id):
  context['tvshow'] = controller.VideoLibrary_GetTVShowDetails(show_id=show_id)
  context['seasons'] = controller.VideoLibrary_GetSeasons(show_id=show_id)
  return render(request, 'kodidj/kodi_server_tv_show.html', context)

@GetPlaylist
@ServerDownRedirect
def tvseason(request, controller, context, show_id, season_id):
  context['tvshow'] = controller.VideoLibrary_GetTVShowDetails(show_id=show_id)
  context['season'] = season_id
  unsorted_episode_list = controller.VideoLibrary_GetEpisodes(show_id=show_id, season_id=season_id)
  context['episodes'] = sorted(unsorted_episode_list, key=itemgetter('episode'))
  return render(request, 'kodidj/kodi_server_tv_season.html', context)

@GetPlaylist
@ServerDownRedirect
def tvepisode(request, controller, context, show_id, season_id, episode_id):
  context['tvshow'] = controller.VideoLibrary_GetTVShowDetails(show_id=show_id)
  context['season'] = season_id

  unsorted_episode_list = controller.VideoLibrary_GetEpisodes(show_id=show_id, season_id=season_id)

  episode_list = sorted(unsorted_episode_list, key=itemgetter('episode'))

  for episode in episode_list:
    if int(episode['episodeid']) == int(episode_id):
      active_episode = episode

  context.update({'activeepisode' : active_episode,
                  'episodes'      : episode_list})

  return render(request, 'kodidj/kodi_server_tv_season.html', context)

@GetPlaylist
@ServerDownRedirect
def movies_index(request, controller, context):
  GetMovieList(controller, context)
  return render(request, 'kodidj/kodi_server_movies.html', context)

@GetPlaylist
@ServerDownRedirect
def movie(request, context, movie_id):
  GetMovieList(controller, context, movie_id)
  return render(request, 'kodidj/kodi_server_movies.html', context)

@GetPlaylist
@ServerDownNoRedirect
def getplaylist(request, controller, context):
  return render(request, 'kodidj/kodi_playlist_panel.html', context)

@GetController
def playmovie(request, controller, context, movie_id):
  controller.Playlist_Clear(playlistType='video')
  controller.Playlist_Add(playlistType='video', params={'item':{'movieid':int(movie_id)}})
  movieInfo = controller.VideoLibrary_GetMovieDetails(movie_id=movie_id)
  controller.Player_Open(playlistType='video')
  controller.Player_Seek(position=movieInfo['resume']['percentage'])
  #controller.Player_Open(params={'item':{'movieid':int(movie_id)}, "options" : {"resume" : True}})
  return getplaylist(request, context['server'].id)

@GetController
def addmovie(request, controller, context, movie_id):
  controller.Playlist_Add(playlistType='video', params={'item':{'movieid':int(movie_id)}})
  return getplaylist(request, context['server'].id)

@GetController
def watchedmovie(request, controller, context, movie_id):
  url = request.get_full_path().replace('_watched', '')
  movieInfo = controller.VideoLibrary_GetMovieDetails(movie_id=movie_id)

  if movieInfo['playcount'] > 0:
    playcount = 0
  else:
    playcount = 1

  controller.VideoLibrary_SetMovieDetails(movie_id=movie_id, playcount=playcount)
  return HttpResponse(status=200)

@GetController
def starredmovie(request, controller, context, movie_id):
  url = request.get_full_path().replace('/{}_starred'.format(movie_id), '')

  starred_movie_id_list = GetStarredMovie()

  if int(movie_id) in starred_movie_id_list:
    RemoveStarredMovie(movie_id)
  else:
    AddStarredMovie(movie_id)

  return redirect(url)

@GetController
def removemovie(request, controller, context, movie_id):
  url = request.get_full_path().replace('/{}_remove'.format(movie_id), '')
  controller.VideoLibrary_RemoveMovie(movie_id=movie_id)
  return redirect(url)

@GetController
def playtv(request, controller, context, show_id, season_id, episode_id):
  controller.Playlist_Clear(playlistType='video')
  controller.Playlist_Add(playlistType='video', params={'item':{'episodeid':int(episode_id)}})
  episodeInfo = controller.VideoLibrary_GetEpisodeDetails(episode_id=episode_id)
  controller.Player_Open(playlistType='video')
  controller.Player_Seek(position=episodeInfo['resume']['percentage'])
  #controller.Player_Open(params={'item':{'episodeid':int(episode_id)}, "options" : {"resume" : True}})
  return getplaylist(request, context['server'].id)

@GetController
def addtv(request, controller, context, show_id, season_id, episode_id):
  controller.Playlist_Add(playlistType='video', params={'item':{'episodeid':int(episode_id)}})
  return getplaylist(request, context['server'].id)

@GetController
def watchedtv(request, controller, context, show_id, season_id, episode_id):
  url = request.get_full_path().replace('_watched', '')
  episodeInfo = controller.VideoLibrary_GetEpisodeDetails(episode_id=episode_id)

  if episodeInfo['playcount'] > 0:
    playcount = 0
  else:
    playcount = 1

  controller.VideoLibrary_SetEpisodeDetails(episode_id=episode_id, playcount=playcount)
  return HttpResponse(status=200)

@GetController
def removetvepisode(request, controller, context, show_id, season_id, episode_id):
  url = request.get_full_path().replace('/{}_remove'.format(episode_id), '')
  controller.VideoLibrary_RemoveEpisode(episode_id=episode_id)
  return redirect(url)

@GetController
def removetvshow(request, controller, context, show_id):
  url = request.get_full_path().replace('/{}_remove'.format(show_id), '')
  controller.VideoLibrary_RemoveTVShow(show_id=show_id)
  return redirect(url)

@GetController
def starredtvshow(request, controller, context, show_id):
  url = request.get_full_path().replace('/{}_starred'.format(show_id), '')

  starred_tv_id_list = GetStarredTV()

  if int(show_id) in starred_tv_id_list:
    RemoveStarredTV(show_id)
  else:
    AddStarredTV(show_id)

  return redirect(url)

@GetController
def watchedtvseason(request, controller, context, show_id, season_id):
  url = request.get_full_path().replace('/{}_watched'.format(season_id), '')

  seasons = controller.VideoLibrary_GetSeasons(show_id=show_id)

  for season in seasons:
    if int(season['season']) == int(season_id):
      active_season = season

  if active_season['playcount'] > 0:
    playcount = 0
  else:
    playcount = 1

  unsorted_episode_list = controller.VideoLibrary_GetEpisodes(show_id=show_id, season_id=season_id)
  episode_list = sorted(unsorted_episode_list, key=itemgetter('episode'))

  for episode in episode_list:
    controller.VideoLibrary_SetEpisodeDetails(episode_id=episode['episodeid'], playcount=playcount)

  return redirect(url)

@GetController
def playpause(request, controller, context):
  # Revisit this, doesn't play if stopped
  controller.Player_PlayPause()
  return HttpResponse(status=200)

@GetController
def stop(request, controller, context):
  controller.Player_Stop()
  return getplaylist(request, context['server'].id)

@GetController
def forward(request, controller, context):
  controller.Player_SetSpeed(speed='increment')
  return HttpResponse(status=200)

@GetController
def backward(request, controller, context):
  controller.Player_SetSpeed(speed='decrement')
  return HttpResponse(status=200)

@GetController
def skip(request, controller, context):
  # goto next item in playlist ?
  controller.Player_Seek(position=100)
  return getplaylist(request, context['server'].id)

@GetController
def restart(request, controller, context):
  # get current position
  # if 0 Player.GoTo previous item in playlist
  controller.Player_Seek(position=0)
  return HttpResponse(status=200)

@GetController
def mute(request, controller, context):
  controller.Application_SetMute()
  return HttpResponse(status=200)

@GetController
def togglesubtitles(request, controller, context):
  properties = controller.Player_GetProperties()
  if properties['subtitleenabled']:
    mode = 'off'
  else:
    mode = 'on'
  controller.Player_SetSubtitle(mode=mode)
  return HttpResponse(status=200)

@GetController
def cyclesubtitles(request, controller, context):
  mode = 'next'
  controller.Player_SetSubtitle(mode=mode)
  return HttpResponse(status=200)

@GetController
def remove(request, controller, context, index):
  controller.Playlist_Remove(playlistType='video', index=index)
  return getplaylist(request, context['server'].id)

@GetController
def playlistplay(request, controller, context, index):
  controller.Player_GoTo(index=index)
  return getplaylist(request, context['server'].id)

@GetController
def clear(request, controller, context):
  controller.Playlist_Clear( playlistType='video')
  return getplaylist(request, context['server'].id)

@GetController
def videoscan(request, controller, context):
  controller.VideoLibrary_Scan(show_dialog=True)
  return HttpResponse(status=200)

@GetController
def quit(request, controller, context):
  controller.System_Shutdown()
  return HttpResponseRedirect(reverse('kodi'))

@GetController
def setvolume(request, controller, context):
  try:
    volume = request.GET['volume']
  except:
    pass
  else:
    controller.Application_SetVolume(volume=volume)
  finally:
    return HttpResponse(status=200)

@GetController
def setprogress(request, controller, context, percentage):
  controller.Player_Seek(position=percentage)
  return HttpResponse(status=200)

@GetController
def getstatus(request, controller, context):
  player_properties = controller.Player_GetProperties()
  application_properties = controller.Application_GetProperties()

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
