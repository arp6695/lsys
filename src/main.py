"""
Main frontend for lsys
Prompts for in-file, read and construct lsys objects
    Then prompt for # of iterations
    Draw, wait
Prompt to save the image (defaults to scalable vector img)
Goto 1

The alphabet has preset tokens that automatically correspond to turtle actions:
    'F' - Forward by a given unit (Variable)
    'G' - Forward by a given unit (Constant)
    '+' - Left by the lsys angle
    '-' - Rigth by the lsys angle
    '[' - Push tuple w/ turtle position and angle onto stack
    ']' - Pop tuple w/ turtle position and angle off of stack, reset turtle position & angle
    'X', 'Y', & 'Z' - Generic Constants - no action

Following commands are:
    'load [filename]' or 'l [filename]' -   read and parse lsys objects from a given data file
    'display' or 'd'                    -   print all currently loaded lsys objects
    'help'                              -   print help
    'size [int]' or 's [int]'           -   change the size of the picture (1 by default)
"""

import sys
from turtle import *
from util.Stack import *

def load( filename ):
    """ Open the file at 'filename' and return a collection of lsys objects. """
    # TODO
    pass

def printCollection( lst ):
    """ Print each lsys object in the given list. """
    # TODO
    pass

def help():
    """ Print Help """
    # TODO
    pass

def main():

    size = 1                # Size preset
    lsysCollection = []     # Colleciton of lsys objects currently loaded
    stack = Stack

    # Intro to everything, check for loadable file
    print( "Hello. Welcome to the interpreter frontend for lsys." )
    if( sys.argv.length() == 2 ):
        filename = argv[1]
        try:
            f = open( filename )
            lsysCollection = getFromFile( filename )
            print( "Sucessfully loaded: {}. ".format(filename) )

        except FileNotFoundError:
            print( "Could not open file: {}".format(filename) )
            print( "Usage: \'python3 path/to/main.py path/to/datafile.txt\'" )
    else:
        print( "No file was loaded. Use 'load [filename]' to parse a file for lsys objects." )

    # Main loop
    while True:
        userIN = input( ">" )
        # TODO

if __name__ == "__main__":
    main()
