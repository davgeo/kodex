#!/usr/bin/env python3

''' KODI '''
# Python default package imports

# Third-party package imports
from kodijsonrpc import KodiJSONClient

# Local file imports

#################################################
# GetServer
#################################################
def GetServer(func):
  def wrapper(host, port, user, pwd, *args, **kwargs):
    server = KodiJSONClient(host, port, user, pwd)
    return func(server, *args, **kwargs)
  return wrapper

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
# GetRecentlyAddedEpisodes
#################################################
@GetServer
def RecentlyAddedEpisodes():
  recentEpisodes = server.VideoLibrary.GetRecentlyAddedEpisodes({'properties':['title', 'showtitle', 'thumbnail', 'tvshowid', 'episode', 'season']})
  episodes = recentEpisodes['episodes']
  for episode in episodes:
    thumbnail = urllib.parse.unquote(episode['thumbnail']).replace('image://', '').strip(r'/')
    val = URLValidator()
    try:
      val(thumbnail)
    except ValidationError:
      showDetails = server.VideoLibrary.GetTVShowDetails({'tvshowid': episode['tvshowid'], 'properties':['thumbnail',]})['tvshowdetails']
      thumbnail = urllib.parse.unquote(showDetails['thumbnail']).replace('image://', '').strip(r'/')
      try:
        val(thumbnail)
      except ValidationError:
        thumbnail = 'http://placekitten.com/g/50/50'
    episode['thumbnail'] = thumbnail
  return episodes