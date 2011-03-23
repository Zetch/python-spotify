#!/usr/bin/env python

# *********************************************************************** #
# Spotify Python API - Command line
# Author: Nauzet Hernandez (nauzethc@gmail.com)
# *********************************************************************** #

from spotify.handler import SpotifyHandler 
from optparse import OptionParser


if __name__ == '__main__':    

    spotify_handler = SpotifyHandler()

    parser = OptionParser(usage="usage: %prog [options [arg1]]")

    parser.add_option("-p", "--play-pause",
        action="callback",
        callback=spotify_handler.play_pause, 
        help="Play/Pause current song")

    parser.add_option("-n", "--next",
        action="callback",
        callback=spotify_handler.next, 
        help="Jump to next song")

    parser.add_option("-b", "--previous",
        action="callback",
        callback=spotify_handler.previous,
        help="Jump to previous song")

    parser.add_option("-x", "--stop",
        action="callback",
        callback=spotify_handler.stop,
        help="Stop player")

    parser.add_option("-i", "--info",
        action="callback",
        dest="info", type="str",
        callback=spotify_handler.get_meta,
        help="Show info for given arg")

    parser.add_option("-s", "--status",
        action="callback",
        dest="stat", type="str",
        callback=spotify_handler.get_property,
        help="Show status for given arg")

    parser.add_option("-c", "--cover-path",
        action="callback",
        callback=spotify_handler.fetch_cover,
        help="Get cached cover image path")

    (options, args) = parser.parse_args()
