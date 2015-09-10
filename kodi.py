#!/usr/bin/env python3

''' ANANKE '''
# Python default package imports
import os
import sys
import argparse

# Third-party package imports
from jsonrpcclient.http_server import HTTPServer

# Local file imports

import logging
logging.getLogger('jsonrpcclient').setLevel(logging.INFO)
logging.basicConfig()

#################################################
# KodiServer
#################################################
class KodiServer:
  headers = {'content-type': 'application/json'}
  #logVerbosity = logzila.Verbosity.MINIMAL

  #################################################
  # constructor
  #################################################
  def __init__(self, ident, host, port, user, pwd):
    self.id = ident
    self.server = HTTPServer('http://{0}:{1}/jsonrpc'.format(host,port), headers=self.headers, auth=(user, pwd))

#################################################
# Kodi
#################################################
class Kodi:
  #logVerbosity = logzila.Verbosity.MINIMAL

  #################################################
  # constructor
  #################################################
  def __init__(self):
    self.serverList = []

  # *** CLASSES *** #
  ############################################################################
  # AddServer
  ############################################################################
  def AddServer(self, host, port, user, pwd):
    serverID = len(self.serverList)
    server = KodiServer(serverID, host, port, user, pwd)
    self.serverList.append(server)
    return serverID

  ############################################################################
  # GetActivePlayers
  ############################################################################
  def GetActivePlayers(self, ident):
    resp = self.serverList[ident].server.request('Player.GetActivePlayers')
    print(resp)
    return resp[0]['playerid']

  ############################################################################
  # PlayerPause
  ############################################################################
  def PlayerPause(self, ident, pID):
    resp = self.serverList[ident].server.request('Player.PlayPause', playerid=pID)
    print(resp)





