#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
# Project: github-music-status
# FilePath: /app.py
# File: app.py
# Created Date: Saturday, June 27th 2020, 2:12:09 pm
# Author: Craig Bojko (craig@pixelventures.co.uk)
# -----
# Last Modified: Sun Jul 05 2020
# Modified By: Craig Bojko
# -----
# Copyright (c) 2020 Pixel Ventures Ltd.
# ------------------------------------
# <<licensetext>>
"""

import os
import sys
import http.client
import json

# Add ./vendors to import locations
# Allows lambda to have vendors packaged to local dir
vendors = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(vendors, "./vendor"))

from termcolor import colored
from custom_logging import create_logger

LAST_FM_ORIGIN = "ws.audioscrobbler.com"
LAST_FM_PATH = "/2.0/?method=user.getrecenttracks&user=coffee_manic&limit=3&api_key=c7c4d08a4d66fa11cd3337be949a670d&format=json"

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_GRAPH_ORIGIN = "api.github.com"
GITHUB_GRAPH_PATH = "/graphql"

LOGGER = create_logger(level="INFO", colors=True)


def fetch_last_fm_status():
    """
    Query last_FM and return a list of recent tracks
    """
    data = {}
    try:
        connection = http.client.HTTPSConnection(LAST_FM_ORIGIN, 443)
        connection.request("GET", LAST_FM_PATH)
        response = connection.getresponse()
        LOGGER(
            "Last_FM: Status: {} Reason: {}".format(response.status, response.reason),
            level="debug",
        )

        if response.status == 200:
            data = response.read().decode()
        connection.close()
        return data
    except http.client.HTTPException as error:
        LOGGER("Error fetching Last_FM data", error, level="error")
        return False


def push_github_status(status, expires=False):
    """
    POST a status message to github
    """
    expires_at_str = ('expiresAt: "{}"'.format(expires)) if expires is False else ""
    mutator = """mutation UpdateUserStatus {
        changeUserStatus(
        input: {
            emoji: ":notes:"
            message: \"""" + status + """\"
            """ + expires_at_str + """
        }
        ) {
        clientMutationId
        }
    }"""
    LOGGER("QUERY: ", mutator, level="debug")

    try:
        connection = http.client.HTTPSConnection(GITHUB_GRAPH_ORIGIN, 443)
        headers = {
            "Authorization": "Bearer %s" % GITHUB_TOKEN,
            "User-Agent": "python bot",
            "Content-Type": "application/json",
        }
        connection.request(
            "POST",
            GITHUB_GRAPH_PATH,
            body=json.dumps({"query": mutator}),
            headers=headers,
        )
        response = connection.getresponse()
        data = response.read().decode()
        connection.close()
        LOGGER(
            "Github: Status: {} Reason: {}".format(response.status, response.reason),
            data,
            level="debug",
        )
        return True
    except http.client.HTTPException as error:
        LOGGER("Error pushing Github graph data", error, level="error")
        return error


def main(colors=True):
    """
    Main function - run the app
    """
    json_data = fetch_last_fm_status()
    if json_data is False:
        return False

    data = json.loads(json_data)
    tracks = data.get("recenttracks", {}).get("track")
    now_playing = False
    now_playing_track = None

    for track in tracks:
        try:
            attr = track.get("@attr", {})
            if attr and attr.get("now_playing") == "true":
                now_playing = True
                now_playing_track = track
            else: continue
        except KeyError:
            continue

    now_playing_str = (
        colored(now_playing, "green" if now_playing is True else "red")
        if colors is True
        else now_playing
    )
    if now_playing:
        now_playing_track_data = "Listening to {}: {}".format(
            now_playing_track.get("artist", {}).get("#text"),
            now_playing_track.get("name", ""),
        )
        LOGGER("Now Playing: {}".format(now_playing_str), now_playing_track_data)
        push_github_status(now_playing_track_data)  # , expires="2020-06-28T04:00:00Z")
    else:
        LOGGER("Now Playing: {}".format(now_playing_str))
    return now_playing_track


def lambda_handler(event, context):
    """
    Handler function for AWS Lambda - initial entry point
    """
    global LOGGER
    LOGGER = create_logger(level="DEBUG", colors=False)
    message = main(colors=False)
    return {"now_playing": message}


if __name__ == "__main__":
    main(colors=True)
