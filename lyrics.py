"""
File: lyrics.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Contains functions for searching, processing
and analyzing lyrics
"""

import lyricsgenius as lg
import pandas as pd
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# API Guide https://github.com/johnwmillr/LyricsGenius
genius = lg.Genius("RZ8Yj-QLkMTDtrke4uL3LfKFDrNrFR-XjGG4Ie5-m3s8SUhevqJE6nz3Ym9zxxON")
genius.verbose = False  # Disable printing of status messages
genius.remove_section_headers = True  # Remove section headers from lyrics


def getSong(title, artist):
    song = genius.search_song(title, artist)
    if song is None:
        print("'" + title + "' by", artist, "not found.")
        return None
    print("'" + song.title + "' by", song.artist)
    print("Album:", "'" + song.album + "'")
    return song


def getLyrics(song):
    lyrics = song.lyrics
    print("Lyrics:\n", lyrics)
    return lyrics


def preProcess(lyrics):
    tokenized_lyrics = word_tokenize(lyrics)
    print("\nTokenized:", tokenized_lyrics)

    stop_words = set(stopwords.words("english"))
    stop_filtered = []
    for word in tokenized_lyrics:
        if word not in stop_words:
            stop_filtered.append(word)
    print("Filtered:", stop_filtered)

    lemm_filter = []
    lm = WordNetLemmatizer()
    for word in stop_filtered:
        lemm_filter.append(lm.lemmatize(word))
    print("Lemmatized:", lemm_filter)

    return lemm_filter


def analyze(lyrics):
    lyrics = preProcess(lyrics)

    data = pd.read_csv('dataset/train.tsv', sep='\t')

    tkn = RegexpTokenizer(r'[a-zA-Z0-9]+')
    cv = CountVectorizer(lowercase=True, stop_words="english", tokenizer=tkn.tokenize)
    text_count = cv.fit_transform(data['Phrase'])
    x_train, t_test, y_train, y_test = train_test_split(text_count, data['Sentiment'],
                                                        test_size=0.3, random_state=1)

    return 0
