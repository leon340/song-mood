import spotipy
from secret import *
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def getTrackFeatures(title, artist):
    id = getTrackID(title, artist)
    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # features
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    key = features[0]['key']
    mode = features[0]['mode']
    loudness = features[0]['loudness']

    track = [name, album, artist, release_date, length, popularity, tempo, time_signature, key, mode, loudness]

    return track


def getTrackID(title, artist):
    track_info = title + "+" + artist
    track_info = track_info.replace(" ", "+")
    results = sp.search(q=track_info, type='track')
    return results['tracks']['items'][0]['id']
