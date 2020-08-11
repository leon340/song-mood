"""
File: lyric_weights.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Provide functions to assign weights
lines of lyrics based on the frequency of their occurrence

Not in use currently but may be useful in the future
"""

from difflib import SequenceMatcher


def getWeightMap(lyrics):
    """
    Creates a Python dictionary containing line, weight pairs
    association each line in the lyrics with a weight (how often it occurs)
    :param lyrics: lyrics to create the map from
    :return: the Python dictionary weight map
    """
    weight_map = dict()

    lines = getLines(lyrics)
    total_lines = len(lines)
    for line in lines:
        addLine(line, weight_map)
    for key in weight_map:
        weight_map[key] = weight_map[key]/total_lines
    return weight_map


def getLines(lyric_string):
    """
    Turns the lyrics body of text into a list of lines from the lyrics
    :param lyric_string: The string containing all the lyrics
    :return: list of lines in the lyrics
    """
    lines = lyric_string.split("\n")
    while "" in lines:
        lines.remove("")
    return lines


def addLine(line, map):
    """
    Adds a line to the weight map or if the line is already
    in the map, updates the weight.
    Accounts for similar lines using a sequence matcher so
    that similar lines don't have separate entries and weights
    :param line: line in the lyrics to add
    :param map: weight map to add the line to
    :return: the updated weight map
    """
    for key in map:
        similarity = SequenceMatcher(None, line, key).ratio()
        if similarity >= 0.8:
            map[key] += 1
            return
    map[line] = 1
