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
  kodiControl = kodi.Kodi()
  ident = kodiControl.AddServer('192.168.1.77', '8080', 'xbmc', 'xbmc')
  playerID = kodiControl.GetActivePlayers(ident)
  kodiControl.PlayerPause(ident, playerID)

############################################################################
# default process if run as standalone
############################################################################
if __name__ == "__main__":
  if sys.version_info < (3,4):
    sys.stdout.write("[DM] Incompatible Python version detected - Python 3.4 or greater is required.\n")
  else:
    main()
