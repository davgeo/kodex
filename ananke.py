#!/usr/bin/env python3

''' ANANKE '''
# Python default package imports
import os
import sys
import argparse

# Third-party package imports
import json
import requests

# Local file imports

############################################################################
# main
############################################################################
def main():
  url = 'http://xbmc:xbmc@192.168.1.77:8080/jsonrpc'

  headers = {'content-type': 'application/json'}

  # Example echo method
  payload = {
      "method": "Player.GetActivePlayers",
      "jsonrpc": "2.0",
      "id": 0,
  }
  response = requests.post(
      url, data=json.dumps(payload), headers=headers).json()

  print(response)
  print(response['result'])

  pID = response['result'][0]['playerid']

  print(pID)

  payload = {
      "method": "Player.PlayPause",
      "params": [pID],
      "jsonrpc": "2.0",
      "id": 0,
  }

  response = requests.post(
      url, data=json.dumps(payload), headers=headers).json()

  print(response)
'''
    "Player.GetActivePlayers": {
      "description": "Returns all active players",
      "params": [

      ],
      "returns": {
        "items": {
          "properties": {
            "playerid": {
              "$ref": "Player.Id",
              "required": true
            },
            "type": {
              "$ref": "Player.Type",
              "required": true
            }
          },
          "type": "object"
        },
        "type": "array",
        "uniqueItems": true
      },
      "type": "method"
    },

    "Player.Id": {
      "default": -1,
      "id": "Player.Id",
      "maximum": 2,
      "minimum": 0,
      "type": "integer"
    },

    "Player.PlayPause": {
      "description": "Pauses or unpause playback and returns the new state",
      "params": [
        {
          "$ref": "Player.Id",
          "name": "playerid",
          "required": true
        },
        {
          "$ref": "Global.Toggle",
          "default": "toggle",
          "name": "play"
        }
      ],
      "returns": {
        "$ref": "Player.Speed"
      },
      "type": "method"
    }
'''

############################################################################
# default process if run as standalone
############################################################################
if __name__ == "__main__":
  if sys.version_info < (3,4):
    sys.stdout.write("[DM] Incompatible Python version detected - Python 3.4 or greater is required.\n")
  else:
    main()
