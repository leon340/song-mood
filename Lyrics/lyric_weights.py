"""
File: lyric_weights.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Provide functions to assign weights
lines of lyrics based on the frequency of their occurrence
"""

from difflib import SequenceMatcher

# Attempt to add line to map
# Go through map, if no line has similarity >= 0.8 then add the line to the map, initialize occurrence at 1
# If similar line found, increase the occurrence by one
# After the map has been finished divide each occurrence by the total number of lines to get a weight


def getWeightMap(lyrics):
    weight_map = dict()

    lines = getLines(lyrics)
    total_lines = len(lines)
    for line in lines:
        addLine(line, weight_map)
    for key in weight_map:
        weight_map[key] = weight_map[key]/total_lines
    return weight_map


def getLines(lyric_string):
    lines = lyric_string.split("\n")
    while "" in lines:
        lines.remove("")
    return lines


def addLine(line, map):
    for key in map:
        similarity = SequenceMatcher(None, line, key).ratio()
        if similarity >= 0.8:
            map[key] += 1
            return
    map[line] = 1
