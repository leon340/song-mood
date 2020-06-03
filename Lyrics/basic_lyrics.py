"""
File: basic_lyrics.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Contains functions for searching, processing
and analyzing lyrics
"""

import lyricsgenius as lg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer

# API Guide https://github.com/johnwmillr/LyricsGenius
genius = lg.Genius("RZ8Yj-QLkMTDtrke4uL3LfKFDrNrFR-XjGG4Ie5-m3s8SUhevqJE6nz3Ym9zxxON")
genius.verbose = False  # Disable printing of status messages
genius.remove_section_headers = True  # Remove section headers from lyrics


def getSong(title, artist):
    """
    Retrieves a song from the genius database given a
    title and artist
    :param title: title of a song
    :param artist: artist of the song
    :return: Song if found, if not found, None
    """
    song = genius.search_song(title, artist)
    if song is None:
        print("'" + title + "' by", artist, "not found.")
        return None
    print("'" + song.title + "' by", song.artist)
    if song.album is not None:
        print("Album:", "'" + song.album + "'")
    return song


def getLyrics(song):
    """
    Gets a prints the lyrics of a given song
    type (part of the genius api)
    :param song: song who's lyrics are to be retrieved and printed
    :return: string containing the lyrics of the song
    """
    lyrics = song.lyrics
    print("Lyrics:\n", lyrics)
    return lyrics


def preProcess(lyrics):
    """
    Pre-processes lyrics by tokenizing , removing
    stop words, and lemmatizing them to get them ready
    for sentiment analysis
    :param lyrics: string of lyrics to be pre-processed
    :return: the pre-processed string
    """
    tokenized_lyrics = word_tokenize(lyrics)

    stop_words = set(stopwords.words("english"))
    stop_filtered = []
    for word in tokenized_lyrics:
        if word not in stop_words:
            stop_filtered.append(word)

    lemm_filter = []
    lm = WordNetLemmatizer()
    for word in stop_filtered:
        lemm_filter.append(lm.lemmatize(word))

    processed_lyrics = TreebankWordDetokenizer().detokenize(lemm_filter)

    return processed_lyrics

def analyze(lyrics):
    """
    Runs a sentiment analysis of a given string and prints the result.
    Takes the average of two analyses, nltk's SentimentIntensityAnalyzer
    and textblob's sentiment polarity
    :param lyrics: the string (song lyrics in this case) to be
    analyzed for sentiment
    """
    lyrics = preProcess(lyrics)

    sia = SentimentIntensityAnalyzer()
    sia_sent = sia.polarity_scores(lyrics)

    blob = TextBlob(lyrics)
    blob_sent = blob.sentiment.polarity

    avg_sentiment = (sia_sent['compound'] + blob_sent) / 2
    print("\nAverage Sentiment:", avg_sentiment)

    if -1 <= avg_sentiment < -0.6:
        print("Negative")
    elif -0.6 <= avg_sentiment < -0.3:
        print("Mostly Negative")
    elif -0.3 <= avg_sentiment <= 0.3:
        print("Neutral")
    elif 0.3 < avg_sentiment <= 0.6:
        print("Mostly Positive")
    elif 0.6 < avg_sentiment <= 1:
        print("Positive")
