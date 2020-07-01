#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Project: github-music-status
# FilePath: /app.py
# File: app.py
# Created Date: Saturday, June 27th 2020, 2:12:09 pm
# Author: Craig Bojko (craig@pixelventures.co.uk)
# -----
# Last Modified: Wed Jul 01 2020
# Modified By: Craig Bojko
# -----
# Copyright (c) 2020 Pixel Ventures Ltd.
# ------------------------------------
# <<licensetext>>
###

import os
import sys

# Add ./vendors to import locations
# Allows lambda to have vendors packaged to local dir
vendors = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(vendors, "./vendor")) 

import http.client
import json
from termcolor import colored
from custom_logging import createLogger

lastFmOrigin = 'ws.audioscrobbler.com'
lastFmPath = '/2.0/?method=user.getrecenttracks&user=coffee_manic&limit=3&api_key=c7c4d08a4d66fa11cd3337be949a670d&format=json'

githubToken = os.environ['GITHUB_TOKEN']
githubGraphOrigin = 'api.github.com'
githubGraphQLPath = '/graphql'

COLORS = None # type: boolean

logger = createLogger(level='INFO', colors=COLORS)

def fetchLastFMStatus():
  data = {}
  try:
    connection = http.client.HTTPSConnection(lastFmOrigin, 443)
    connection.request('GET', lastFmPath)
    response = connection.getresponse()
    logger("LastFM: Status: {} Reason: {}".format(response.status, response.reason), type='debug')

    if response.status == 200:
      data = response.read().decode()
    connection.close()
    return data
  except http.client.HTTPException as error:
    logger('Error fetching LastFM data', error, type='error')
    return 

def pushGithubStatus(status, expires=False):
  expiresAtStr = ("expiresAt: \"{}\"".format(expires)) if expires != False else ''
  mutator = """mutation UpdateUserStatus {
    changeUserStatus(
      input: {
        emoji: ":notes:"
        message: \"""" + status + """\"
        """ + expiresAtStr + """
      }
    ) {
      clientMutationId
    }
  }"""
  logger('QUERY: ', mutator, type='debug')

  try:
    connection = http.client.HTTPSConnection(githubGraphOrigin, 443)
    headers = {
      'Authorization' : 'Bearer %s' %  githubToken,
      'User-Agent': 'python bot',
      'Content-Type': 'application/json'
    }
    connection.request('POST', githubGraphQLPath, body=json.dumps({ 'query': mutator }), headers=headers)
    response = connection.getresponse()
    data = response.read().decode()
    connection.close()
    logger("Github: Status: {} Reason: {}".format(response.status, response.reason), data, type='debug')
  except http.client.HTTPException as error:
    logger('Error pushing Github graph data', error, type='error')
    return

def main():
  jsonData = fetchLastFMStatus()
  if jsonData:
    data = json.loads(jsonData)
    tracks = data.get('recenttracks', {}).get('track')
    nowPlaying = False
    nowPlayingTrack = None

    for track in tracks:
      try: 
        attr = track.get('@attr', {})
        if attr and attr.get('nowplaying') == 'true':
          nowPlaying = True
          nowPlayingTrack = track
      except: continue

    # logger('Data: ', data, tracks, type='info')
  
    nowPlayingStr = colored(nowPlaying, 'green' if nowPlaying == True else 'red' ) if COLORS else nowPlaying
    if nowPlaying:
      nowPlayingTrackData = "Listening to {}: {}".format(\
        nowPlayingTrack.get('artist', {}).get('#text'),\
        nowPlayingTrack.get('name', '')\
      )
      logger("Now Playing: {}".format(nowPlayingStr), nowPlayingTrackData)
      pushGithubStatus(nowPlayingTrackData) #, expires="2020-06-28T04:00:00Z")
    else: logger("Now Playing: {}".format(nowPlayingStr))
    return nowPlayingTrack

def lambdaHandler(event, context):
  COLORS = False
  logger = createLogger(level='DEBUG', colors=False)
  message = main()
  return { 'nowPlaying' : message }

if __name__ == "__main__":
  COLORS = True
  main()
