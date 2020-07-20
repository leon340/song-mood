"""
File: songtiment.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Processes command line args and calls
necessary functions accordingly.
"""

import sys
import getopt
from Lyrics import basic_lyrics
from Lyrics import nn_lyrics
from Lyrics import lyric_weights
from Song_Stats import features

def usage():
    """
    Simply prints the usage statement
    """
    print("Usage:")
    print("songtiment.py [-s \"song\"] -a \"artist\"")


def analyze(title, artist):
    """
    Preforms analysis of a song given its title and artist
    :param title: title of the song
    :param artist: artist attributed to the song
    """
    final_sentiment = 0

    # Load the machine learning based model
    modelIMDB = nn_lyrics.loadModel("IMDB")
    encoderIMDB = nn_lyrics.createEncoder("IMDB")
    modelYelp = nn_lyrics.loadModel("Yelp")
    encoderYelp = nn_lyrics.createEncoder("Yelp")

    print("Analyzing", title, "by", artist, "...\n")
    song = basic_lyrics.getSong(title, artist)
    if song is None:
        return

    lyrics_received = basic_lyrics.getLyrics(song)
    print("")
    weight_map = lyric_weights.getWeightMap(lyrics_received)  # Needed for line by line analysis

    # Get and print stats about the song
    feature_vec = features.getTrackFeatures(title, artist)
    features.printFeatures(feature_vec)
    #
    final_sentiment += ((basic_lyrics.analyze(lyrics_received) + 1)/2)  # using x+1/2 to convert to a 0-1 scale
    # print("Title Sentiment: ")
    # final_sentiment += ((basic_lyrics.analyze(title) + 1)/2)
    #
    print("\nIMDB Model:")
    imdb_lyrics = nn_lyrics.predict(lyrics_received, pad=True, model_to_predict=modelIMDB, encoder=encoderIMDB)
    final_sentiment += imdb_lyrics
    print("\nModel lyrics prediction: ", imdb_lyrics)
    # imdb_title = nn_lyrics.predict(title, pad=False, model_to_predict=modelIMDB, encoder=encoderIMDB)
    # final_sentiment += imdb_title
    # print("Model title prediction: ", imdb_title)
    #
    print("\nYelp Model:")
    yelp_lyrics = nn_lyrics.predict(lyrics_received, pad=True, model_to_predict=modelYelp, encoder=encoderYelp)
    final_sentiment += yelp_lyrics
    print("\nModel lyrics prediction: ", yelp_lyrics)
    # yelp_title = nn_lyrics.predict(title, pad=False, model_to_predict=modelYelp, encoder=encoderYelp)
    # final_sentiment += yelp_title
    # print("Model title prediction: ", yelp_title)
    #
    print("\nFinal Sentiment: ", final_sentiment/3)

    # TODO: The above section is where a "formula" would go to calculate the final sentiment


def main():
    """
    songtiment.py [-s "song"] -a "artist"
    Processes command line arguments using getopt
    and calls functions accordingly to preform song analysis
    """
    arguments = sys.argv
    argc = len(arguments)
    if argc == 1:
        usage()
        return

    artist = None
    title = None
    opts, args = getopt.getopt(arguments[1:], "s:a:")
    artist_found = False

    for o, a in opts:
        if o == "-s":
            title = a
        elif o == "-a":
            artist_found = True
            artist = a
        else:
            usage()
            return

    if not artist_found:
        usage()
        return

    if title is not None:
        analyze(title, artist)
    else:
        print("Analyzing music by", artist, "...\n")
        print("Analysis of full discography not yet implemented.")


main()
