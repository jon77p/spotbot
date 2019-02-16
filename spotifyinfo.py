import spotipy
import sys
import os
import pprint
import requests
import re

def tokenreauth():
    infile = open('../secret', 'r')
    f = infile.readlines()
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + f[0].strip()}
    data = {'grant_type': 'refresh_token', 'refresh_token': f[1].strip()}
    infile.close()
    req = requests.post(url, headers=headers, data=data)
    res = req.json()
    outfile = open('../auth_token', 'w')
    outfile.write(res['access_token'])
    outfile.close()
    return tokenreader()

def tokenreader():
    readfile = open('../auth_token', 'r')
    out = readfile.readline().strip()
    readfile.close()
    return out

def tokeneval(intoken):
    try:
        spotify = spotipy.Spotify(auth=intoken)
    except Exception as e:
        print('exception in tokeneval!!! ', e)
        tokenreauth()
        return tokenreader()
    return intoken

def info(token, logfile):
    url = open(logfile, 'r').readlines()[-1]
    regex = '(?<=[\"]spotify:track:)([A-Za-z0-9])*|(Playback:((Started)|(Halted)))'

    pattern = re.compile(regex, re.IGNORECASE)
    match = pattern.search(str(url))
    if match:
        url = match.group(0)
    else:
        count = -1
        while match is None:
            url = open(logfile, 'r').readlines()[count]
            match = pattern.search(str(url))
            count -= 1
        url = match

    spotify = spotipy.Spotify(auth=token)

    try:
        track = spotify.track(url)
    except Exception as e:
        track = {"name": "N/A", "artists": [{"name": "N/A"}], "album": {"images": [{"url": "static/img/spotify_connect.png"}]}, "external_urls": {"spotify": "N/A"}}
    return {"track": track["name"], "artist": track["artists"][0]["name"], "img": track["album"]["images"][0]["url"], "uri": track["uri"]}
