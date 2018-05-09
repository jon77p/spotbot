import spotipy
import sys
import os
import pprint

#try:
#    url = sys.argv[1]
#except:
#    print('Error! Expected track URI identifier')
#    exit()

#url = input().split()[3]
url = open('/home/pi/raspotify.log', 'r').readlines()[-1].split()[-1][1:-1]
url = str(url)
#print(url)

token = os.getenv('SPOTIFY_ACCESS_TOKEN')

spotify = spotipy.Spotify(auth=token)

track = spotify.track(url)

#pprint.pprint(track)
print 'Track Name:', track["name"]
print 'Artist:', track["artists"][0]["name"]
print 'Image:', track["album"]["images"][0]["url"]

def info():
    url = open('/home/pi/raspotify.log', 'r').readlines()[-2].split()[-1][1:-1]
    url = str(url)
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    spotify = spotipy.Spotify(auth=token)
    track = spotify.track(url)
    return track["name"], track["artists"][0]["name"], track["album"]["images"][0]["url"]
