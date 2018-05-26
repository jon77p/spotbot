import spotipy
import sys
import os
import pprint
import requests

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
    except:
        print('exception in tokeneval!!! ', e)
        tokenreauth()
        return tokenreader()
    return intoken

def info(token):
    url = open('/home/pi/raspotify.log', 'r').readlines()[-1].split()[-1][1:-1]
    url = str(url)
    while url == "aspotify" or url == "oade":
        url = open('/home/pi/raspotify.log', 'r').readlines()[-1].split()[-1][1:-1]
        url = str(url)

    if url == "layback:Halte" or url == "layback:Starte":
        url = str('invalid')

    spotify = spotipy.Spotify(auth=token)

    try:
        track = spotify.track(url)
    except Exception as e:
        print(e)
        track = {"name": "N/A", "artists": [{"name": "N/A"}], "album": {"images": [{"url": "static/img/spotify_connect.png"}]}, "external_urls": {"spotify": "N/A"}}
    return track["name"], track["artists"][0]["name"], track["album"]["images"][0]["url"], track["external_urls"]["spotify"]
