#!/usr/bin/env python

import lastfm
import taglib
import os


def flacProfileDir(dir):
    dirprof = {'TITLE': [], 'TRACKNUMBER': []}
    for dirpath, dirname, files in os.walk(dir):
        for filen in files:
            if filen.endswith('.flac'):
                filepath = os.path.join(dirpath, filen)
                flacfile = taglib.File(filepath)
                tags = flacfile.tags
                for key in tags:
                    if key not in dirprof:
                        dirprof[key] = {}
                    if key == 'TITLE':
                        dirprof[key].append(tags[key][0])
                    elif key == 'TRACKNUMBER':
                        tracknumber = int(tags[key][0])
                        dirprof[key].append(tracknumber)
                    else:
                        if tags[key][0] not in dirprof[key]:
                            dirprof[key][tags[key][0]] = 0
                        dirprof[key][tags[key][0]] += 1
    return dirprof


def analyze(profile):
    result = {'tracks': len(profile['TRACKNUMBER']), 'artist': {}, 'date': {}, 'album': {}, 'genre': {}}
    for artist in profile['ARTIST']:
        result['artist'][artist] = float(profile['ARTIST'][artist])/result['tracks']
    for date in profile['DATE']:
        result['date'][date] = float(profile['DATE'][date])/result['tracks']
    for album in profile['ALBUM']:
        result['album'][album] = float(profile['ALBUM'][album])/result['tracks']
    for genre  in profile['GENRE']:
        result['genre'][genre] = float(profile['GENRE'][genre])/result['tracks']
    return result

sampledirprofile = flacProfileDir('/home/alex/git/agent-runkle/sampleflac/samplealbum/')

print('sample dir profile:', sampledirprofile)
analyzedprof = analyze(sampledirprofile)
print(analyzedprof)

guessedalbum = max(analyzedprof['album'], key=lambda k: analyzedprof['album'][k])
guessedartist = max(analyzedprof['artist'], key=lambda k: analyzedprof['artist'][k])

x = lastfm.api('./creds.json')
pm = {}
pm['method'] = 'album.search'
pm['album'] = guessedalbum

searchresults = x.doCall(pm)
print(searchresults['results']['albummatches']['album'][0])
print(searchresults['results']['albummatches']['album'][1])


#f = taglib.File("")
