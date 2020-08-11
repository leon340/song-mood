"""
File: equation.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Calculate the final sentiment of a song
given various attributes of the song
"""

"""
Weights from:
Jamdar, A., Abraham, J., Khanna, K., &amp; Dubey, R. (2015). Emotion Analysis of Songs Based on Lyrical 
and Audio Features. International Journal of Artificial Intelligence &amp; Applications, 6(3), 35-50. 
doi:10.5121/ijaia.2015.6304
"""
MODE_WEIGHT = 0.50
TEXT_WEIGHT = 1.0
LYRIC_WEIGHT = 0.75
TITLE_WEIGHT = 0.25
LOUDNESS_WEIGHT = 0.7
TEMPO_WEIGHT = 0.8
TOTAL_WEIGHT = MODE_WEIGHT + TEXT_WEIGHT + LOUDNESS_WEIGHT + TEMPO_WEIGHT


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
                       (TEMPO_WEIGHT * tempoSentiment(tempo))) / TOTAL_WEIGHT
    return final_sentiment


def textSentiment(lyric_sentiment, title_sentiment):
    """
    Calculates a weighted average of the sentiment of the lyrics and title of a song
    Functions as determining the sentiment of all of the text associated with the song
    :param lyric_sentiment: sentiment of the lyrics (0-1 scale)
    :param title_sentiment: sentiment of the title (0-1 scale)
    :return: Sentiment of the text with the song
    """
    return (LYRIC_WEIGHT * lyric_sentiment) + (TITLE_WEIGHT * title_sentiment)


def tempoSentiment(bpm):
    """
    Applies an equation obtained via exponential regression that predicts the
    song's sentiment given its BPM
    See feature_research or readme for more info about the equation
    :param bpm: bpm of the song
    :return: predicted sentiment of the song
    """
    bpm_valence = 0.0000300856076 * 1.08493613 ** bpm
    if bpm_valence > 1:
        return 1
    return bpm_valence


def loudnessSentiment(dB):
    """
    Applies an equation obtained via exponential regression
    that predicts the song's sentiment given its average loudness in dB
    See feature_research or readme for more info about the equation
    :param dB: average loudness of the song in dB
    :return: predicted sentiment of the song
    """
    loudness_valence = 2.31657085 * 1.161360103 ** dB
    if loudness_valence > 1:
        return 1
    return loudness_valence
