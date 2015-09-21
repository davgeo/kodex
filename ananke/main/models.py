from django.db import models
from .kodijsonrpc import KodiJSONClient

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import urllib

# Create your models here.
class Server(models.Model):
  name = models.CharField(max_length=200)
  host = models.CharField(max_length=200)
  port = models.CharField(max_length=200)
  user = models.CharField(max_length=200)
  pwd = models.CharField(max_length=200)

  def __str__(self):
    return '{0} {1}:{2}'.format(self.name, self.host, self.port)

  def CheckStatus(self):
    server = KodiJSONClient(self.host, self.port, self.user, self.pwd)
    try:
      server.JSONRPC.Ping()
    except:
      return 'Offline'
    else:
      return 'Online'

  def GetRecentlyAddedEpisodes(self):
    server = KodiJSONClient(self.host, self.port, self.user, self.pwd)
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


class Config(models.Model):
  activeServer = models.ForeignKey('Server')
  thumbnails = models.BooleanField()

  def __str__(self):
    return 'Active Server = {0}\n'.format(self.activeServer) \
         + 'Thumbnails = {0}'.format(self.thumbnails)
