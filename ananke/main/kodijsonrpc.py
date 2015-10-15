#!/usr/bin/env python3

''' KODI JSON RPC Client '''
# Python default package imports

# Third-party package imports
from jsonrpcclient.http_server import HTTPServer

# Local file imports

# Enable logging on jsconrpcclient module
import logging
logging.getLogger('jsonrpcclient').setLevel(logging.INFO)
logging.basicConfig()

KODI_JSON_NAMESPACES = ["VideoLibrary",
                        "Settings",
                        "Favourites",
                        "AudioLibrary",
                        "Application",
                        "Player",
                        "Input",
                        "System",
                        "Playlist",
                        "Addons",
                        "AudioLibrary",
                        "Files",
                        "GUI" ,
                        "JSONRPC",
                        "PVR",
                        "xbmc"]

#################################################
#
# KodiNamespace
#
#################################################
class KodiNamespace(object):
  #################################################
  # __init__
  #################################################
  def __init__(self):
    self.server = None

  #################################################
  # __getattr__
  # catch undefined methods
  #################################################
  def __getattr__(self, name):
    className = self.__class__.__name__

    if self.server is None:
      print("No server instantiated in {0}".format(className))
      return None

    method = name
    kodiMethod = "{0}.{1}".format(className, method)

    def func(*args, **kwargs):
      print(className, method, kodiMethod, *args, **kwargs)
      resp = self.server.request(kodiMethod, *args, **kwargs)
      #print(resp)
      return resp
    return func

  #################################################
  # UpdateServer
  #################################################
  def UpdateServer(self, server):
    self.server = server

# Dynamic create classes for all namespaces
for namespace in KODI_JSON_NAMESPACES:
  newClass = "class {0}(KodiNamespace):\n\t\tpass\n".format(namespace)
  exec (newClass)


#################################################
#
# KodiJSONClient
#
#################################################
class KodiJSONClient(object):
  headers = {'content-type': 'application/json'}

  #################################################
  # __init__
  #################################################
  def __init__(self, host, port, user, pwd):
    self._AddNamespaces()
    self._SwitchServer(host, port, user, pwd)

  ############################################################################
  # _AddNamespaces
  # Dynamically add namespace classes
  ############################################################################
  def _AddNamespaces(self):
    for namespace in KODI_JSON_NAMESPACES:
      s = "self.{0} = {0}()".format(namespace)
      exec(s)

  ############################################################################
  # _SwitchServer
  # Switch or set server
  ############################################################################
  def _SwitchServer(self, host, port, user, pwd):
    self.url = 'http://{0}:{1}/'.format(host, port)
    self.server = HTTPServer(self.GetUrl('jsonrpc'), headers=self.headers, auth=(user, pwd))
    for namespace in KODI_JSON_NAMESPACES:
      s = "self.{0}.UpdateServer(self.server)".format(namespace)
      exec(s)

  ############################################################################
  # GetUrl
  # Get url to current active server
  ############################################################################
  def GetUrl(self, path=''):
    return self.url + path

