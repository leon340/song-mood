"""
File: features.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Extract and display information about songs using the Spotify API

Spotipy tutorial used as a guideline: https://morioh.com/p/31b8a607b2b0
"""

import spotipy
from secret import *
from spotipy.oauth2 import SpotifyClientCredentials

# Setup and authorize Spotify API
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def getTrackFeatures(title, artist):
    """
    Creates a feature vector for a song
    :param title: Title of the song
    :param artist: Artist for the song
    :return: Feature vector containing information about the song
    Feature vector format: [name, album, artist, release_date, length, tempo, key, mode, loudness]
    """
    id = getTrackID(title, artist)
    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta data
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']

    # features
    tempo = features[0]['tempo']
    key = features[0]['key']
    mode = features[0]['mode']
    loudness = features[0]['loudness']

    track = [name, album, artist, release_date, length, tempo, key, mode, loudness]

    return track


def getTrackID(title, artist):
    """
    Searches for and retrieves the Spotify track ID for a song
    Will always take the first result in the Spotify search
    :param title: Title of the song
    :param artist: Artist for the song
    :return: The song's track ID
    """
    track_info = title + " " + artist
    # track_info = track_info.replace(" ", "+")
    results = sp.search(q=track_info, type='track')
    return results['tracks']['items'][0]['id']


def printFeatures(feature_vec):
    """
    Prints a given song feature vector in a more readable format
    :param feature_vec: the feature vector to format and print
    """
    # Represents standard pitch class notation
    pitch_classes = ["C", "C#/D♭", "D", "D#/E♭", "E", "F", "F#/G♭", "G",
                     "G#/A♭", "A", "A#/B♭", "B", "Key not detected"]
    mode_types = ["Minor", "Major"]
    name = feature_vec[0]
    album = feature_vec[1]
    artist = feature_vec[2]
    release = feature_vec[3]
    length = int(feature_vec[4])
    tempo = feature_vec[5]
    key = int(feature_vec[6])
    mode = int(feature_vec[7])
    loudness = feature_vec[8]

    print("\nStats for {} on {} by {}:".format(name, album, artist))
    print("Released on {}".format(release))
    print("Length: {} seconds".format(length/1000))  # Convert from ms to seconds
    print("Tempo: {}bpm".format(tempo))
    print("Key: {}".format(pitch_classes[key]))
    print("Mode: {}".format(mode_types[mode]))
    print("Average Loudness: {}db".format(loudness))

