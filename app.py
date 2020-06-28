
import os
import http.client
import json
from termcolor import colored
from custom_logging import log

lastFmOrigin = 'ws.audioscrobbler.com'
lastFmPath = '/2.0/?method=user.getrecenttracks&user=coffee_manic&limit=3&api_key=c7c4d08a4d66fa11cd3337be949a670d&format=json'

githubToken = os.environ['GITHUB_TOKEN']
githubGraphOrigin = 'api.github.com'
githubGraphQLPath = '/graphql'

def fetchLastFMStatus():
  data = {}
  try:
    connection = http.client.HTTPSConnection(lastFmOrigin, 443)
    connection.request('GET', lastFmPath)
    response = connection.getresponse()
    log("LastFM: Status: {} Reason: {}".format(response.status, response.reason), type='debug')

    if response.status == 200:
      data = response.read().decode()
    connection.close()
    return data
  except http.client.HTTPException as error:
    log('Error fetching LastFM data', error, type='error')
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
  log('QUERY: ', mutator, type='debug')

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
    log("Github: Status: {} Reason: {}".format(response.status, response.reason), data, type='debug')
  except http.client.HTTPException as error:
    log('Error pushing Github graph data', error, type='error')
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

    # log('Data: ', data, tracks, type='info')
    nowPlayingTrackData = "Listening to {}: {}"\
      .format(\
        nowPlayingTrack.get('artist', {}).get('#text'),\
        nowPlayingTrack.get('name', '')\
      )\
      if nowPlaying else ''

    log("Now Playing: {}".format(colored(nowPlaying, 'green' if nowPlaying == True else 'red' )), nowPlayingTrackData)
    if nowPlaying: pushGithubStatus(nowPlayingTrackData) #, expires="2020-06-28T04:00:00Z")

if __name__ == "__main__":
  main()

