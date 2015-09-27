#!/usr/bin/env python3

''' KODI '''
# Python default package imports
import urllib

# Third-party package imports
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

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
# ProcessURL
#################################################
def ProcessURL(url):
  url = urllib.parse.unquote(url).strip(r'/')
  val = URLValidator()

  try:
    val(url)
  except ValidationError:
    return ''
  else:
    return url

#################################################
# ProcessThumbnail
#################################################
def ProcessThumbnail(thumbnail):
  url = ProcessURL(thumbnail.replace('image://', ''))

  if url:
    return url
  else:
    return ''

#################################################
# ProcessThumbnails
#################################################
def ProcessThumbnails(thumbnailList, tvEpisode=False, server=None):
  for item in thumbnailList:
    thumbnail = ProcessThumbnail(item['thumbnail'])

    if tvEpisode and thumbnail == '':
      showDetails = server.VideoLibrary.GetTVShowDetails({'tvshowid': item['tvshowid'], 'properties':['thumbnail',]})['tvshowdetails']
      thumbnail = ProcessThumbnail(showDetails['thumbnail'])

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
                          'lastplayed',
                          'resume']}

  response = server.VideoLibrary.GetEpisodes(params)
  episodes = response['episodes']
  ProcessThumbnails(episodes, tvEpisode=True, server=server)
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
  ProcessThumbnails(movies)
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
  ProcessThumbnails(episodes, tvEpisode=True, server=server)
  return episodes

@GetServer
def VideoLibrary_GetRecentlyAddedMovies(server):
  params = {'properties':['title',
                          'thumbnail']}
  recentMovies = server.VideoLibrary.GetRecentlyAddedMovies(params)
  movies = recentMovies['movies']
  ProcessThumbnails(movies)
  return movies

@GetServer
def VideoLibrary_GetRecentlyAddedMusicVideos(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetSeasonDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetSeasons(server, show_id):
  params = {'tvshowid':int(show_id),
            'properties':['season',
                          'tvshowid',
                          'thumbnail']}
  response = server.VideoLibrary.GetSeasons(params)
  seasons = response['seasons']
  ProcessThumbnails(seasons)
  return seasons

@GetServer
def VideoLibrary_GetTVShowDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetTVShows(server):
  params = {'properties':['title',
                          'thumbnail']}
  response = server.VideoLibrary.GetTVShows(params)
  tvshows = response['tvshows']
  ProcessThumbnails(tvshows)
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
def Player_GetActivePlayers(server):
  raise NotImplementedError

@GetServer
def Player_GetItem(server):
  raise NotImplementedError

@GetServer
def Player_GetPlayers(server):
  raise NotImplementedError

@GetServer
def Player_GetProperties(server):
  raise NotImplementedError

@GetServer
def Player_GoTo(server):
  raise NotImplementedError

@GetServer
def Player_Move(server):
  raise NotImplementedError

@GetServer
def Player_Open(server):
  raise NotImplementedError

@GetServer
def Player_PlayPause(server):
  raise NotImplementedError

@GetServer
def Player_Rotate(server):
  raise NotImplementedError

@GetServer
def Player_Seek(server):
  raise NotImplementedError

@GetServer
def Player_SetAudioStream(server):
  raise NotImplementedError

@GetServer
def Player_SetPartymode(server):
  raise NotImplementedError

@GetServer
def Player_SetRepeat(server):
  raise NotImplementedError

@GetServer
def Player_SetShuffle(server):
  raise NotImplementedError

@GetServer
def Player_SetSpeed(server):
  raise NotImplementedError

@GetServer
def Player_SetSubtitle(server):
  raise NotImplementedError

@GetServer
def Player_Stop(server):
  raise NotImplementedError

@GetServer
def Player_Zoom(server):
  raise NotImplementedError
