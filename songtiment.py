"""
File: songtiment.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Processes command line args and calls
necessary functions accordingly
"""

import sys
import getopt
import lyrics


def usage():
    """
    Simply prints the usage statement
    """
    print("Usage:")
    print("songtiment.py [-s \"song\"] -a \"artist\"")


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
        print("Analyzing", title, "by", artist, "...\n")
        song = lyrics.getSong(title, artist)
        if song is None:
            return
        lyrics_received = lyrics.getLyrics(song)
        lyrics.analyze(lyrics_received)
    else:
        print("Analyzing music by", artist, "...\n")
        print("Analysis of full discography not yet implemented.")


main()