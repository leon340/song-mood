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

all_tracks = top_playlist['tracks']['items'] + happy_playlist['tracks']['items'] + sad_playlist['tracks']['items'] \
             + eighties_playlist['tracks']['items'] + jazz_playlist['tracks']['items'] + \
             country_playlist['tracks']['items'] + classical_playlist['tracks']['items'] + \
             rock_playlist['tracks']['items'] + rnb_playlist['tracks']['items'] + metal_playlist['tracks']['items'] \
             + blues_playlist['tracks']['items'] + latin_playlist['tracks']['items']

HAPPY_THRESHOLD = 0.75
SAD_THRESHOLD = 0.25


def avgAll(feature):
    """
    Finds the average of a given feature over the entire all_tracks data set
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
    print("All ", feature, "tempo happy avg: ", avg / total)


def analysisSad(feature):
    """
    Finds the average of a given feature over sad songs in the all_tracks data set
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
    print("All ", feature, "tempo sad avg: ", avg / total)


analysisHappy('tempo')
analysisSad('tempo')
avgAll('tempo')

analysisHappy('loudness')
analysisSad('loudness')
avgAll('loudness')
