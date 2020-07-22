"""
File: equation.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Calculate the final sentiment of a song
given various attributes of the song
"""

"""
Formula inputs: Mode, Lyric Sentiment, Title Sentiment, Loudness, Tempo
Output: Scale of how happy or sad the song is
Some sort of weighted average

Weights from:
Jamdar, A., Abraham, J., Khanna, K., &amp; Dubey, R. (2015). Emotion Analysis of Songs Based on Lyrical 
and Audio Features. International Journal of Artificial Intelligence &amp; Applications, 6(3), 35-50. 
doi:10.5121/ijaia.2015.6304

Mode: 0.5
Valence(Lyrics and Title): 1.0
Loudness: 0.7
Tempo: 0.8

Mode is already given by Spotify as 1 being major and 0 being minor
"""


def sentiment(mode, lyric_sentiment, title_sentiment, loudness, tempo):
    return None


def tempo(bpm):
    """
    Find bpm of an average song, that will be 0.5
    to the same with very happy song, that will be 1.0
    do it again with sad song, that will be 0.0
    now create a formula given bpm to put it somewhere in that 0.0-1.0 range
    :param bpm:
    :return:
    """
    return None


def loudness(dbs):
    """
    Find avg loudness(dbs) of an average song, that will be 0.5
    to the same with very happy song, that will be 1.0
    do it again with sad song, that will be 0.0
    now create a formula given avg dbs to put it somewhere in that 0.0-1.0 range
    :param dbs:
    :return:
    """
    return None
