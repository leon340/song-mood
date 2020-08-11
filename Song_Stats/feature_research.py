"""
File: feature_research.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Analyze features of songs in correlation
to their valence
"""

import spotipy
from secret import *
from spotipy.oauth2 import SpotifyClientCredentials

# Setup and authorize Spotify API
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Top 50 playlist
top_playlist = sp.playlist("37i9dQZEVXbMDoHDwVN2tF")

# Happy hits playlist
happy_playlist = sp.playlist("37i9dQZF1DXdPec7aLTmlC")

# Life sucks playlist
sad_playlist = sp.playlist("37i9dQZF1DX3YSRoSdA634")

# 80's Smash Hits
eighties_playlist = sp.playlist("19PgP2QSGPcm6Ve8VhbtpG")

# Jazz Classics
jazz_playlist = sp.playlist('37i9dQZF1DXbITWG1ZJKYt')

# Country's Greatest Hits: The '90s
country_playlist = sp.playlist('37i9dQZF1DXaiEFNvQPZrM')

# Classical Essentials
classical_playlist = sp.playlist('37i9dQZF1DWWEJlAGA9gs0')

# Rock Classics
rock_playlist = sp.playlist('37i9dQZF1DWXRqgorJj26U')

# I Love My '00s R&B
rnb_playlist = sp.playlist('37i9dQZF1DWYmmr74INQlb')

# Metal Essentials
metal_playlist = sp.playlist('37i9dQZF1DWWOaP4H0w5b0')

# Blues Classics
blues_playlist = sp.playlist('37i9dQZF1DXd9rSDyQguIk')

# Latin Pop Classics
latin_playlist = sp.playlist('37i9dQZF1DX6ThddIjWuGT')

# Diverse data set of over 1000 songs
all_tracks = top_playlist['tracks']['items'] + happy_playlist['tracks']['items'] + sad_playlist['tracks']['items'] \
             + eighties_playlist['tracks']['items'] + jazz_playlist['tracks']['items'] + \
             country_playlist['tracks']['items'] + classical_playlist['tracks']['items'] + \
             rock_playlist['tracks']['items'] + rnb_playlist['tracks']['items'] + metal_playlist['tracks']['items'] \
             + blues_playlist['tracks']['items'] + latin_playlist['tracks']['items']

# Minimum valence needed for the song to be considered happy
HAPPY_THRESHOLD = 0.75
# Maximum valence needed for the song to be considered sad
SAD_THRESHOLD = 0.25


def avgAll(feature):
    """
    Finds the average of a given feature over the entire all_tracks data set
    Also prints the number of songs calculated in the average
    :param feature: the aspect of the song to average EX: Loudness, tempo
    """
    total = 0
    avg = 0
    for track in all_tracks:
        total += 1
        id = track['track']['id']
        features = sp.audio_features(id)
        tempo = features[0][feature]
        avg += float(tempo)

    print("All tracks total: ", total)
    print("All tracks avg ", feature, ": ", avg/total)


def analysisHappy(feature):
    """
    Finds the average of a given feature over happy songs in the all_tracks data set
    Also prints the number of songs calculated in the average
    :param feature: the aspect of the song to average EX: Loudness, tempo
    """
    total = 0
    avg = 0
    for track in all_tracks:
        id = track['track']['id']
        features = sp.audio_features(id)
        val = features[0]['valence']
        val = float(val)
        if val >= HAPPY_THRESHOLD:  # valence greater than or equal to what is considered happy valence
            total += 1
            tempo = features[0][feature]
            avg += float(tempo)
    print("All ", feature, "happy total: ", total)
    print("All ", feature, "happy avg: ", avg / total)


def analysisSad(feature):
    """
    Finds the average of a given feature over sad songs in the all_tracks data set
    Also prints the number of songs calculated in the average
    :param feature: the aspect of the song to average EX: Loudness, tempo
    """
    total = 0
    avg = 0
    for track in all_tracks:
        id = track['track']['id']
        features = sp.audio_features(id)
        val = features[0]['valence']
        val = float(val)
        if val <= SAD_THRESHOLD:  # valence less than or equal to what is considered sad valence
            total += 1
            tempo = features[0][feature]
            avg += float(tempo)
    print("All ", feature, "sad total: ", total)
    print("All ", feature, "sad avg: ", avg / total)


"""
Find bpm of an average song, that will be a 0.5 sentiment
to the same with very happy song, that will be a 1.0 sentiment
do it again with sad song, that will be a 0.0 sentiment

0.25 and 0.75 valence thresholds:
All tempo happy total:  239
All tempo happy avg:  124.40260669456072
All tempo sad total:  213
All tempo sad avg:  109.87290140845074

0.10 and 0.90 valence thresholds:
All tempo happy total:  70
All tempo happy avg:  126.98902857142858
All tempo sad total:  82
All tempo sad avg:  100.2535609756097

All tracks total:  1007
All tracks avg:  119.32066236345577

Regression equation calculated using the points above:
0.0000300856076(1.08493613)^x
"""
analysisHappy('tempo')
analysisSad('tempo')
avgAll('tempo')


"""
Find avg loudness(dB) of an average song, that will be a 0.5 sentiment
to the same with very happy song, that will be a 1.0 sentiment
do it again with sad song, that will be a 0.0 sentiment
    
0.25 and 0.75 valence thresholds:
All  loudness happy total:  239
All  loudness happy avg:  -7.873564853556487
All  loudness sad total:  213
All  loudness sad avg:  -15.483995305164322

0.10 and 0.90 valence thresholds:
All  loudness happy total:  70
All  loudness happy avg:  -8.150214285714284
All  loudness sad total:  82
All  loudness sad avg:  -21.327012195121956

All tracks total:  1007
All tracks avg  loudness :  -9.934176762661364

Regression equation calculated using the points above:
2.31657085(1.161360103)^x
"""
analysisHappy('loudness')
analysisSad('loudness')
avgAll('loudness')
