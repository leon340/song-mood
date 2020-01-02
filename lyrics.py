"""
File: lyrics.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Contains functions for searching, processing
and analyzing lyrics
"""

import lyricsgenius as lg

genius = lg.Genius("RZ8Yj-QLkMTDtrke4uL3LfKFDrNrFR-XjGG4Ie5-m3s8SUhevqJE6nz3Ym9zxxON")
genius.verbose = False  # Disable printing of status messages
genius.remove_section_headers = True  # Remove section headers from lyrics


def getSong(name, artist):
    song = genius.search_song(name, artist)
    print(song.title, "by", song.artist, "on the album", song.album)
    return song


def getLyrics(song):
    lyrics = song.lyrics
    print(lyrics)
    return lyrics


def analyze(lyrics):
    return 0
