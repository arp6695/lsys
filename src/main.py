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
    'B' - Backward by a given unit (Constant)
    '+' - Left by the lsys angle
    '-' - Rigth by the lsys angle
    '[' - Push tuple w/ turtle position and angle onto stack
    ']' - Pop tuple w/ turtle position and angle off of stack, reset turtle position & angle
    '0' & '1' - Forward and then backward
    'A', 'B', 'C', 'X', 'Y', & 'Z' - Generic Constants - no action

Following commands are:
    'load [file]' or 'l [file]'         -   Read and parse lsys objects from a given data file
                                            (example files exist in src/data/)
    'display' or 'd'                    -   Print all currently loaded lsys objects
    'run [lsys name]'                   -   Run recursions on a loaded lsys object, uses python's turtle
    'help'                              -   Print this help screen
    'size [int]' or 's [int]'           -   Change the size of the picture (1 by default)
    'exit' or 'quit' or 'q'             -   Quit the program

TODO: Enable stochasticism (redo [slightly] the parsing, allow for variability)
"""

import sys
from turtle import *
from util.IO import *
from util.Stack import *

STACK = getStack()

def turtleInit():
    """ Initialize the turtle module """
    tracer(0,0) # Refresh the drawing manually, must use turtle.update() at the end
    # delay(0) # NOTE: This is an alternative to tracer, w/ no need for update()
    reset()
    setworldcoordinates( -300, -300, 300, 300 ) # NOTE: This may cause problems

def chooseAction( token, size, angle=0 ):
    """
    Determine which turtle action to use.
    Helper for recursive turtle implementation
    param: token - a string, token from lsys alphabet
    param: size - an integer, the length the turtle will go forward
    param: angle - an integer, the angle associated with the lsys
    """
    global STACK

    # Defaults
    if token == "F" or token == "G":
        forward( size )
    elif token == "-":
        right( angle )
    elif token == "+":
        left( angle )

    # Stack related
    elif token == "[":
        STACK.push( (getpos(), heading()) )
    elif token == "]":
        tpl = STACK.pop()
        setpos( tpl[0] )
        seth( tpl[1] )

    # Fractal Tree related
    elif token == "1":      # Draw a line segment and return
        forward( size )
        backward( size )
    elif token == "0":      # Draws a line segment 'leaf'
        forward(size)
        lt(45)
        forward(size/2)
        backward(size/2)
        rt(90)
        forward(size/2)
        backward(size/2)
        lt(45)
        backward(size)
    return None

def runLsys( lsys, n, size ):
    """
    Recursive function that recurses a given number of times, and determines turtle action.
    lsys - an lsys object
    n - a integer, number of recursions
    """
    runLsysHelper( lsys.getAxiom(), lsys, n, size )

def runLsysHelper( string, lsys, n, size ):
    """
    Recursive Helper for 'runLsys'
    """
    for char in string:
        if n <= 0:
            chooseAction( char, size, lsys.getAngle() )
        else:
            runLsysHelper( lsys.transformRule( char ), lsys, n-1, size )
    return None

def printCollection( lst ):
    """ Print each lsys object in the given list. """

    if len(lst) == 0:
        return

    for obj in lst:
        print("-" * 20)
        print(obj)
    print("-" * 20)

def printHelp():
    """ Print Help """
    for line in open("src/help.txt"):
        print(line)

def main():
    size = 1
    lsysCollection = list()     # Colleciton of lsys objects currently loaded

    # Intro to everything, check for loadable file
    print( "Hello. Welcome to the interpreter frontend for lsys." )
    if( len(sys.argv) == 2 ):
        filename = sys.argv[1]
        try:
            f = open( filename )
            lsysCollection = getLsysFromFile( filename )
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
        cmdTerm = userIN.strip(" ").split(" ")[0].lower()
        if( len(userIN.split(" ")) == 2 ):
            param = userIN.split(" ")[1]
        else:
            param = None

        # Determine what should be done w/ the command term and param
        if cmdTerm == 'l' or cmdTerm == 'load':
            if param == None:
                print( "Invalid use of 'load'. Usage \'load [filename]\'" )
                continue
            lsysCollection += getLsysFromFile( param )

        elif cmdTerm == 'help' or cmdTerm == 'h':
            printHelp()

        elif cmdTerm == 'display' or cmdTerm == 'd':
            printCollection( lsysCollection )

        elif cmdTerm == 'size' or cmdTerm == 's':
            if not param.isdigit():
                print( "Invalid use of 'size'. Usage \'size [filename]\'" )
            else:
                size = int(param)
                print( "Size is now set to %d.", size )

        elif cmdTerm == 'run' or cmdTerm == 'r':
            for obj in lsysCollection:
                if obj.getName() == param:
                    print("Found an lsys called '%s'. ", endl="")
                    try:
                        n = int(input("How many recursions would you like? "))
                        turtleInit()
                        runLsys( lsys, n, size )
                        toSave = input("Image Generated. Would you like to save it? (y/n)").lower()
                        if toSave == "y":

                            # TODO Save here.
                            print("Saved.")

                    except ValueError:
                        print("That is not a valid number of recursions. Aborting...")
                        break
                    break
            #print("That lsys does not seem to be loaded.")
            pass

        elif cmdTerm == 'exit' or cmdTerm == 'quit' or cmdTerm == 'q':
            exit()

        else:
            print("Unknown command: '%s'", cmdTerm  )

if __name__ == "__main__":
    main()
