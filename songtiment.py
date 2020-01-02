"""
File: songtiment.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Processes command line args and calls
necessary functions accordingly
"""

import sys
import getopt


def usage():
    print("Usage:")
    print("songtiment.py [-s song] -a artist")


def main():
    arguments = sys.argv
    argc = len(arguments)
    if argc == 1:
        usage()
        return

    artist = None
    song = None
    opts, args = getopt.getopt(arguments[1:], "s:a:")
    artist_found = False

    for o, a in opts:
        if o == "-s":
            song = a
        elif o == "-a":
            artist_found = True
            artist = a
        else:
            usage()
            return

    if not artist_found:
        usage()
        return

    if song is not None:
        print("Analyzing", song, "by", artist)
    else:
        print("Analyzing music by", artist)


main()