#!/usr/bin/env python3

''' KODI '''
# Python default package imports
import urllib
import re

# Local file imports
from .kodijsonrpc import KodiJSONClient

#################################################
# GetServer
#################################################
def GetServer(func):
  def wrapper(host, port, user, pwd, *args, **kwargs):
    server = KodiJSONClient(host, port, user, pwd)
    return func(server, *args, **kwargs)
  return wrapper

#################################################
# GetActivePlayer
#################################################
def GetActivePlayer(func):
  def wrapper(server, *args, **kwargs):
    try:
      player_id = server.Player.GetActivePlayers()[0]['playerid']
    except:
      return []
    else:
      return func(server, player_id, *args, **kwargs)
  return wrapper

#################################################
# GetPlaylists
#################################################
def GetPlaylists(func):
  def wrapper(server, playlistType, *args, **kwargs):
    response = server.Playlist.GetPlaylists()
    for playlist in response:
      if playlist['type'] == playlistType:
        playlist_id = playlist['playlistid']
    return func(server, playlist_id, *args, **kwargs)
  return wrapper

#################################################
# ProcessThumbnail
#################################################
def ProcessThumbnail(server, thumbnail):
  url = server.GetUrl('image/') + urllib.parse.quote_plus(thumbnail)

  try:
    re.findall(r'.jpg', url)[0]
  except IndexError:
    return ''
  else:
    return url

#################################################
# ProcessThumbnails
#################################################
def ProcessThumbnails(server, thumbnailList, tvEpisode=False):
  for item in thumbnailList:
    thumbnail = ProcessThumbnail(server, item['thumbnail'])

    if tvEpisode and thumbnail == '':
      showDetails = server.VideoLibrary.GetTVShowDetails({'tvshowid': item['tvshowid'], 'properties':['thumbnail',]})['tvshowdetails']
      thumbnail = ProcessThumbnail(server, showDetails['thumbnail'])

    if thumbnail == '':
      thumbnail = 'http://placekitten.com/g/50/50'

    item['thumbnail'] = thumbnail

#################################################
# Status
#################################################
@GetServer
def Status(server):
  try:
    server.JSONRPC.Ping()
  except:
    return 'Offline'
  else:
    return 'Online'

#################################################
# VideoLibrary
#################################################
@GetServer
def VideoLibrary_Clean(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_Export(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetEpisodeDetails(server, episode_id):
  raise NotImplementedError
  '''params = {'episodeid':int(episode_id),
            'properties':['title',
                          'plot',
                          'showtitle',
                          'thumbnail',
                          'tvshowid',
                          'episode',
                          'season',
                          'lastplayed',
                          'resume']}

  response = server.VideoLibrary.GetEpisodeDetails(params)
  return response'''

@GetServer
def VideoLibrary_GetEpisodes(server, show_id, season_id):
  params = {'tvshowid':int(show_id),
            'season':int(season_id),
            'properties':['title',
                          'plot',
                          'showtitle',
                          'thumbnail',
                          'tvshowid',
                          'episode',
                          'season',
                          'playcount',
                          'lastplayed',
                          'resume',
                          'file']}

  response = server.VideoLibrary.GetEpisodes(params)
  episodes = response['episodes']

  for item in episodes:
    item['episode'] = int(item['episode'])

  ProcessThumbnails(server, episodes, tvEpisode=True)
  return episodes

@GetServer
def VideoLibrary_GetGenres(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetMovieDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetMovieSetDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetMovieSets(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetMovies(server):
  params = {'properties':['title',
                          'lastplayed',
                          'thumbnail',
                          'plot']}
  recentMovies = server.VideoLibrary.GetMovies(params)
  movies = recentMovies['movies']
  ProcessThumbnails(server, movies)
  return movies

@GetServer
def VideoLibrary_GetMusicVideoDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetMusicVideos(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetRecentlyAddedEpisodes(server):
  params = {'properties':['title',
                          'showtitle',
                          'thumbnail',
                          'tvshowid',
                          'episode',
                          'season']}

  recentEpisodes = server.VideoLibrary.GetRecentlyAddedEpisodes(params)
  episodes = recentEpisodes['episodes']
  ProcessThumbnails(server, episodes, tvEpisode=True)
  return episodes

@GetServer
def VideoLibrary_GetRecentlyAddedMovies(server):
  params = {'properties':['title',
                          'thumbnail']}
  recentMovies = server.VideoLibrary.GetRecentlyAddedMovies(params)
  movies = recentMovies['movies']
  ProcessThumbnails(server, movies)
  return movies

@GetServer
def VideoLibrary_GetRecentlyAddedMusicVideos(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetSeasonDetails(server, season_id):
  '''params = {'seasonid':int(season_id),
            'properties':['title',
                          'thumbnail',
                          'plot']}'''
  raise NotImplementedError

@GetServer
def VideoLibrary_GetSeasons(server, show_id):
  params = {'tvshowid':int(show_id),
            'properties':['season',
                          'showtitle',
                          'playcount',
                          'episode',
                          'fanart',
                          'thumbnail',
                          'tvshowid',
                          'watchedepisodes',
                          'art']}

  response = server.VideoLibrary.GetSeasons(params)
  seasons = response['seasons']
  ProcessThumbnails(server, seasons)
  return seasons

@GetServer
def VideoLibrary_GetTVShowDetails(server, show_id):
  params = {'tvshowid':int(show_id),
            'properties':['title',
                          'thumbnail',
                          'plot']}
  response = server.VideoLibrary.GetTVShowDetails(params)
  tvshowdetails = response['tvshowdetails']
  ProcessThumbnails(server, (tvshowdetails, ))
  return tvshowdetails

@GetServer
def VideoLibrary_GetTVShows(server):
  params = {'properties':['title',
                          'thumbnail']}
  response = server.VideoLibrary.GetTVShows(params)
  tvshows = response['tvshows']
  ProcessThumbnails(server, tvshows)
  return tvshows

@GetServer
def VideoLibrary_RemoveEpisode(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_RemoveMovie(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_RemoveMusicVideo(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_RemoveTVShow(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_Scan(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_SetEpisodeDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_SetMovieDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_SetMovieSetDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_SetMusicVideoDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_SetSeasonDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_SetTVShowDetails(server):
  raise NotImplementedError

#################################################
# Player
#################################################
@GetServer
@GetActivePlayer
def Player_GetItem(server, player_id):
  params = {"playerid": player_id,
            "properties": ["uniqueid"]}
  response = server.Player.GetItem(params)
  return response['item']

@GetServer
@GetActivePlayer
def Player_GetPlayers(server, player_id):
  raise NotImplementedError

@GetServer
@GetActivePlayer
def Player_GetProperties(server, player_id):
  params = {"playerid": player_id,
            "properties": ["type",
                           "partymode",
                           "speed",
                           "time",
                           "percentage",
                           "totaltime",
                           "playlistid",
                           "position",
                           "repeat",
                           "shuffled",
                           "canseek",
                           "canchangespeed",
                           "canmove",
                           "canzoom",
                           "canrotate",
                           "canshuffle",
                           "canrepeat",
                           "currentaudiostream",
                           "audiostreams",
                           "subtitleenabled",
                           "currentsubtitle",
                           "subtitles",
                           "live"]}
  return server.Player.GetProperties(params)

@GetServer
@GetActivePlayer
def Player_GoTo(server, player_id):
  raise NotImplementedError

@GetServer
@GetActivePlayer
def Player_Move(server, player_id):
  raise NotImplementedError

@GetServer
@GetActivePlayer
def Player_Open(server, player_id):
  raise NotImplementedError

@GetServer
@GetActivePlayer
def Player_PlayPause(server, player_id):
  response = server.Player.PlayPause({"playerid":player_id})
  return response['speed']

@GetServer
@GetActivePlayer
def Player_Rotate(server, player_id):
  raise NotImplementedError

@GetServer
@GetActivePlayer
def Player_Seek(server, player_id, position):
  params = {"playerid": player_id}
  params['value'] = {'percentage': position}
  response = server.Player.Seek(params)

@GetServer
@GetActivePlayer
def Player_SetAudioStream(server, player_id):
  raise NotImplementedError

@GetServer
@GetActivePlayer
def Player_SetPartymode(server, player_id):
  raise NotImplementedError

@GetServer
@GetActivePlayer
def Player_SetRepeat(server, player_id):
  raise NotImplementedError

@GetServer
@GetActivePlayer
def Player_SetShuffle(server, player_id):
  raise NotImplementedError

@GetServer
@GetActivePlayer
def Player_SetSpeed(server, player_id, speed):
  params = {"playerid": player_id,
            "speed": speed}
  response = server.Player.SetSpeed(params)

@GetServer
@GetActivePlayer
def Player_SetSubtitle(server, player_id):
  raise NotImplementedError
  #Player_GetProperties(server, player_id)
  #params = {"playerid": player_id,
  #          "subtitle": "next",
  #          "enable": toggle}
  #response = server.Player.SetSubtitle(params)

@GetServer
@GetActivePlayer
def Player_Stop(server, player_id):
  response = server.Player.Stop({"playerid":player_id})

@GetServer
@GetActivePlayer
def Player_Zoom(server, player_id):
  raise NotImplementedError

#################################################
# Playerlist
#################################################
@GetServer
@GetPlaylists
def Playlist_Add(server, playlist_id, params):
  params.update({'playlistid':int(playlist_id)})
  response = server.Playlist.Add(params)

@GetServer
@GetPlaylists
def Playlist_Clear(server, playlist_id):
  params = {'playlistid':int(playlist_id)}
  response = server.Playlist.Clear(params)

@GetServer
@GetPlaylists
def Playlist_GetItems(server, playlist_id):
  params = {'playlistid':int(playlist_id),
            'properties':['title',
                          'showtitle',
                          'thumbnail',
                          'tvshowid',
                          'episode',
                          'season',
                          'uniqueid']}

  response = server.Playlist.GetItems(params)

  try:
    episodes = response['items']
  except KeyError:
    episodes = []
  else:
    ProcessThumbnails(server, episodes, tvEpisode=True)

  return episodes

@GetServer
def Playlist_GetProperties(server):
  raise NotImplementedError

@GetServer
def Playlist_Insert(server):
  raise NotImplementedError

@GetServer
@GetPlaylists
def Playlist_Remove(server, playlist_id, index):
  params = {'playlistid':int(playlist_id),
            'position':int(index)}
  response = server.Playlist.Remove(params)

@GetServer
def Playlist_Swap(server):
  raise NotImplementedError

#################################################
# Application
#################################################
@GetServer
def Application_GetProperties(server):
  raise NotImplementedError

@GetServer
def Application_Quit(server):
  raise NotImplementedError

@GetServer
def Application_SetMute(server):
  params = {"mute": "toggle"}
  response = server.Application.SetMute(params)

@GetServer
def Application_SetVolume(server):
  raise NotImplementedError