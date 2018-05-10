import spotipy
import sys
import os
import pprint
import requests

url = open('/home/pi/raspotify.log', 'r').readlines()[-1].split()[-1][1:-1]
url = str(url)

def tokenreauth():
    infile = open('../secret', 'r')
    f = infile.readlines()
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + f[0].strip()}
    data = {'grant_type': 'refresh_token', 'refresh_token': f[1].strip()}
    infile.close()
    req = requests.post(url, headers=headers, data=data)
    res = req.json()
    print(res)
    print(res['access_token'])
    #return res['access_token']
    outfile = open('../auth_token', 'w')
    outfile.write(res['access_token'])
    outfile.close()
    return tokenreader()

def tokenreader():
    readfile = open('../auth_token', 'r')
    out = readfile.readline().strip()
    readfile.close()
    return out

token = tokenreader()

try:
    spotify = spotipy.Spotify(auth=token)
except:
    token = tokenreader()
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
    except Exception as e:
        print('exception in tokeneval!!! ', e)
        tokenreauth()
        return tokenreader()
    return intoken

def info(token):
    url = open('/home/pi/raspotify.log', 'r').readlines()[-2].split()[-1][1:-1]
    url = str(url)
    while url == "oade" or url == "aspotify" or url == "US" or url == "ccurre":
        url = open('/home/pi/raspotify.log', 'r').readlines()[-2].split()[-1][1:-1]
        url = str(url)
    try:
        spotify = spotipy.Spotify(auth=token)
    # this may be totally unneccesary below...
    except Exception as e:
        print('exception!!!! ', e)
        token = tokenreader()
        print(token)
        spotify = spotipy.Spotify(auth=token)

    track = spotify.track(url)
    return track["name"], track["artists"][0]["name"], track["album"]["images"][0]["url"]
