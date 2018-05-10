import spotipy
import sys
import os
import pprint
import requests

url = open('/home/pi/raspotify.log', 'r').readlines()[-1].split()[-1][1:-1]
url = str(url)

def tokenreauth():
    f = open('../secret', 'r').readlines()
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + f[0].strip()}
    data = {'grant_type': 'refresh_token', 'refresh_token': f[1].strip()}
    req = requests.post(url, headers=headers, data=data)
    res = req.json()
    print(res)
    print(res['access_token'])
    return res['access_token']

token = tokenreauth()

try:
    spotify = spotipy.Spotify(auth=token)
except:
    token = tokenreauth()
    spotify = spotipy.Spotify(auth=token)

track = spotify.track(url)

#pprint.pprint(track)
#print 'Track Name:', track["name"]
#print 'Artist:', track["artists"][0]["name"]
#print 'Image:', track["album"]["images"][0]["url"]

def tokeneval(intoken):
#    print(intoken)
    try:
        spotify = spotipy.Spotify(auth=intoken)
    except:
        return tokenreauth()
    return intoken

def info(token):
    url = open('/home/pi/raspotify.log', 'r').readlines()[-2].split()[-1][1:-1]
    url = str(url)
    while url == "oade" or url == "aspotify" or url == "US" or url == "ccurre":
        url = open('/home/pi/raspotify.log', 'r').readlines()[-2].split()[-1][1:-1]
        url = str(url)
    try:
        spotify = spotipy.Spotify(auth=token)
    except Exception as e:
        print(e)
        token = tokenreauth()
        print(token)
        spotify = spotipy.Spotify(auth=token)

    track = spotify.track(url)
    return track["name"], track["artists"][0]["name"], track["album"]["images"][0]["url"]
