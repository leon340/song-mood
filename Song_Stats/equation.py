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

MODE_WEIGHT = 0.50
TEXT_WEIGHT = 1.0
LYRIC_WEIGHT = 0.75
TITLE_WEIGHT = 0.25
LOUDNESS_WEIGHT = 0.7
TEMPO_WEIGHT = 0.8


def sentiment(mode, lyric_sentiment, title_sentiment, loudness, tempo):
    """
    Calculates the weighted final sentiment of a song given
    its features
    :param mode: mode of the song (0 for minor, 1 for major)
    :param lyric_sentiment: sentiment of the lyrics (0-1 scale)
    :param title_sentiment: sentiment of the title (0-1 scale)
    :param loudness: average loudness of the song in dB (usually between -60 and 0)
    :param tempo: tempo of the track in BPM
    :return: the sentiment of the song on a 0-1 scale - 1 being very positive, 0 being negative
    """
    final_sentiment = ((MODE_WEIGHT * mode) +
                       (TEXT_WEIGHT * textSentiment(lyric_sentiment, title_sentiment)) +
                       (LOUDNESS_WEIGHT * loudnessSentiment(loudness)) +
                       (TEMPO_WEIGHT * tempoSentiment(tempo))) / 3
    return final_sentiment


def textSentiment(lyric_sentiment, title_sentiment):
    """
    Calculates a weighted average of the sentiment of the lyrics and title of a song
    Functions as determining the sentiment of all of the text associated with the song
    :param lyric_sentiment: sentiment of the lyrics (0-1 scale)
    :param title_sentiment: sentiment of the title (0-1 scale)
    :return: Sentiment of the text dealing with the song
    """
    return (LYRIC_WEIGHT * lyric_sentiment) + (TITLE_WEIGHT * title_sentiment)


def tempoSentiment(bpm):
    """
    Find bpm of an average song, that will be 0.5
    to the same with very happy song, that will be 1.0
    do it again with sad song, that will be 0.0

    0.25 and 0.75 valences
    All tempo happy total:  239
    All tempo happy avg:  124.40260669456072
    All tempo sad total:  213
    All tempo sad avg:  109.87290140845074

    0.10 and 0.90 valences
    All tempo happy total:  70
    All tempo happy avg:  126.98902857142858
    All tempo sad total:  82
    All tempo sad avg:  100.2535609756097

    All tracks total:  1007
    All tracks avg:  119.32066236345577

    0.0000300856076(1.08493613)^x
    :param bpm: bpm of the song
    :return: predicted sentiment of the song
    """
    bpm_valence = 0.0000300856076 * 1.08493613 ** bpm
    if bpm_valence > 1:
        return 1
    return bpm_valence


def loudnessSentiment(dB):
    """
    Find avg loudness(dB) of an average song, that will be 0.5
    to the same with very happy song, that will be 1.0
    do it again with sad song, that will be 0.0

    0.25 and 0.75 valences
    All  loudness happy total:  239
    All  loudness tempo happy avg:  -7.873564853556487
    All  loudness sad total:  213
    All  loudness tempo sad avg:  -15.483995305164322

    0.10 and 0.90 valences
    All  loudness happy total:  70
    All  loudness tempo happy avg:  -8.150214285714284
    All  loudness sad total:  82
    All  loudness tempo sad avg:  -21.327012195121956

    All tracks total:  1007
    All tracks avg  loudness :  -9.934176762661364
    :param dB: average loudness of the song in dB
    :return: predicted sentiment of the song
    """
    loudness_valence = 2.31657085 * 1.161360103 ** dB
    if loudness_valence > 1:
        return 1
    return loudness_valence
