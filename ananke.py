#!/usr/bin/env python3

''' ANANKE '''
# Python default package imports
import os
import sys
import argparse

# Third-party package imports

# Local file imports
import kodi

############################################################################
# main
############################################################################
def main():
  host = '192.168.1.68' #'192.168.1.77'
  xbmc = kodi.Kodi(host, '8080', 'xbmc', 'xbmc')
  playerID = xbmc.Player.GetActivePlayers()[0]['playerid']
  #xbmc.Player.PlayPause({"playerid":playerID})
  xbmc.JSONRPC.Ping()

############################################################################
# default process if run as standalone
############################################################################
if __name__ == "__main__":
  if sys.version_info < (3,4):
    sys.stdout.write("[DM] Incompatible Python version detected - Python 3.4 or greater is required.\n")
  else:
    main()
