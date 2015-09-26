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
def VideoLibrary_GetEpisodeDetails(server):
  raise NotImplementedError

@GetServer
def VideoLibrary_GetEpisodes(server):
  raise NotImplementedError

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
  params = {'properties':["title",
                          "lastplayed",
                          "thumbnail"]}

  recentMovies = server.VideoLibrary.GetMovies(params)
  movies = recentMovies['movies']
  for movie in movies:
    thumbnail = ProcessThumbnail(movie['thumbnail'])

    if thumbnail == '':
      thumbnail = 'http://placekitten.com/g/50/50'

    movie['thumbnail'] = thumbnail

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
  for episode in episodes:
    thumbnail = ProcessThumbnail(episode['thumbnail'])

    if thumbnail == '':
      showDetails = server.VideoLibrary.GetTVShowDetails({'tvshowid': episode['tvshowid'], 'properties':['thumbnail',]})['tvshowdetails']
      thumbnail = ProcessThumbnail(showDetails['thumbnail'])

      if thumbnail == '':
        thumbnail = 'http://placekitten.com/g/50/50'

    episode['thumbnail'] = thumbnail

  return episodes

@GetServer
def VideoLibrary_GetRecentlyAddedMovies(server):
  params = {'properties':["title",
                          "thumbnail"]}

  recentMovies = server.VideoLibrary.GetRecentlyAddedMovies(params)
  movies = recentMovies['movies']
  for movie in movies:
    thumbnail = ProcessThumbnail(movie['thumbnail'])

    if thumbnail == '':
      thumbnail = 'http://placekitten.com/g/50/50'

    movie['thumbnail'] = thumbnail

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
  for season in seasons:
    thumbnail = ProcessThumbnail(season['thumbnail'])

    if thumbnail == '':
      thumbnail = 'http://placekitten.com/g/50/50'

    season['thumbnail'] = thumbnail

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
  for tvshow in tvshows:
    thumbnail = ProcessThumbnail(tvshow['thumbnail'])

    if thumbnail == '':
      thumbnail = 'http://placekitten.com/g/50/50'

    tvshow['thumbnail'] = thumbnail

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


