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
Valence(Lyrics and Title): 1.0 - maybe split this 75-25?
Loudness: 0.7
Tempo: 0.8

Mode is already given by Spotify as 1 being major and 0 being minor
"""


def sentiment(mode, lyric_sentiment, title_sentiment, loudness, tempo):
    # 0.5(mode) + 0.75(lyric_sentiment) + 0.25(title_sentiment) + 0.7(loudness) + 0.8(tempo)   /   3
    # 0.5(mode) + 1.0(words(lyric_sentiment, title_sentiment)) + 0.7(loudness) + 0.8(tempo)   /   3
    return None


def tempo(bpm):
    """
    Find bpm of an average song, that will be 0.5
    to the same with very happy song, that will be 1.0
    do it again with sad song, that will be 0.0
    now create a formula given bpm to put it somewhere in that 0.0-1.0 range

    0.25 and 0.75 valences
    All tempo happy total:  239
    All tempo happy avg:  124.40260669456072
    All tempo sad total:  213
    All tempo sad avg:  109.87290140845074

    0.9 and 0.10 valences
    All tempo happy total:  70
    All tempo happy avg:  126.98902857142858
    All tempo sad total:  82
    All tempo sad avg:  100.2535609756097

    All tracks total:  1007
    All tracks avg:  119.32066236345577
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

    0.25 and 0.75 valences
    All  loudness happy total:  239
    All  loudness tempo happy avg:  -7.873564853556487
    All  loudness sad total:  213
    All  loudness tempo sad avg:  -15.483995305164322

    0.9 and 0.10 valences
    All  loudness happy total:  70
    All  loudness tempo happy avg:  -8.150214285714284
    All  loudness sad total:  82
    All  loudness tempo sad avg:  -21.327012195121956

    All tracks total:  1007
    All tracks avg  loudness :  -9.934176762661364
    :param dbs:
    :return:
    """
    return None
