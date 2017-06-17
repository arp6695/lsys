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
    'run [lsys name]'                   -   Create a picture for the lsys
    'help'                              -   print help
    'size [int]' or 's [int]'           -   change the size of the picture (1 by default)
    'exit' or 'quit' or 'q'             -   Quit
"""

import sys
from turtle import *
from util.IO import *
from util.Stack import *

SIZE = 1
STACK = getStack()
ANGLE = 90

def chooseAction( token ):
    """ Determine which action to use, given a string token. """
    global SIZE, STACK, ANGLE
    if token == "F" or token == "G":
        forward( SIZE )
    elif token == "-":
        right( ANGLE )
    elif token == "+":
        left( ANGLE )
    elif token == "[":
        STACK.push( (getpos(), heading()) )
    elif token == "]":
        tpl = STACK.pop()
        setpos( tpl[0] )
        seth( tpl[1] )

    return None

def load( filename ):
    """ Open the file at 'filename' and return a collection of lsys objects. """
    # TODO
    pass

def printCollection( lst ):
    """ Print each lsys object in the given list. """
    # TODO
    pass

def printHelp():
    """ Print Help """
    print( "TODO" )

def main():
    global SIZE
    lsysCollection = dict()     # Colleciton of lsys objects currently loaded

    # Intro to everything, check for loadable file
    print( "Hello. Welcome to the interpreter frontend for lsys." )
    if( len(sys.argv) == 2 ):
        filename = sys.argv[1]
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

        # Prompt, extract command term and params
        userIN = input( ">" )
        cmdTerm = userIN.split(" ")[0].lower()
        if( len(userIN.split(" ")) == 2 ):
            param = userIN.split(" ")[1]
        else:
            param = None

        # Determine what should be done w/ the command term and param
        if cmdTerm == 'l' or cmdTerm == 'load':
            if param == None:
                print( "Invalid use of 'load'. Usage \'load [filename]\'" )
                continue
            load( param )

        elif cmdTerm == 'help' or cmdTerm == 'h':
            printHelp()

        elif cmdTerm == 'display' or cmdTerm == 'd':
            printCollection( lsysCollection )

        elif cmdTerm == 'size' or cmdTerm == 's':
            if not param.isdigit():
                print( "Invalid use of 'size'. Usage \'size [filename]\'" )
                continue
            SIZE = int(param)

        elif cmdTerm == 'run' or cmdTerm == 'r':
            # TODO
            pass

        elif cmdTerm == 'exit' or cmdTerm == 'quit' or cmdTerm == 'q':
            exit()
            
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
