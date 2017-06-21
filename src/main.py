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

import sys                  # For Command Line Arguments
from turtle import *        # For Drawing

#from lsys import *
from util.IO import *       # For Reading/Writing lsys to/from files
from util.Stack import *    # For stack support

import datetime             # For naming images
import canvasvg             # For saving images; NOTE: This is a non-standard module -> 'pip install canvasvg'

STACK = getStack()

def turtleInit():
    """ Initialize the turtle module """
    tracer(False) # Refresh the drawing manually, must use turtle.update() at the end
    reset()
    setworldcoordinates( -300, -300, 300, 300 ) # NOTE: This may cause problems on different resolutions
    hideturtle()

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
        data = tuple( [position(), heading()] )
        STACK.push( data )
    elif token == "]":
        tpl = STACK.pop()
        penup()
        setpos( tpl[0] )
        seth( tpl[1] )
        pendown()

    # Fractal Tree related
    elif token == "1":      # Draw a line segment and return
        forward( size )
        #backward( size )
    elif token == "0":      # Draws a line segment 'leaf'
        forward(size)
        """
        lt(45)
        forward(size/4)
        backward(size/4)
        rt(90)
        forward(size/4)
        backward(size/4)
        lt(45)
        backward(size)
        """

    #update()
    return None

def runLsys( l, n, size ):
    """
    Recursive function that recurses a given number of times, and determines turtle action.
    lsys - an lsys object
    n - a integer, number of recursions
    """
    runLsysHelper( l.getAxiom(), l, n, size )

def runLsysHelper( string, l, n, size ):
    """
    Recursive Helper for 'runLsys'
    """
    for char in string:
        if n <= 0 or char not in l.getRuleset().keys():
            chooseAction( char, size, l.getAngle() )
        else:
            runLsysHelper( l.transformRule( char ), l, n-1, size )
    return None

def printCollection( lst ):
    """ Print each lsys object in the given list. """

    if len(lst) == 0:
        print("No lsys objects have been loaded.")
    else:
        print("Currently loaded objects are:")
        for i in range(len(lst)):
            print( "{}. {}".format( str(i+1), lst[i].getName()) )

def printHelp():
    """ Print Help: read help.txt """
    for line in open("src/help.txt"):
        print(line, end="")

def main():
    size = 2
    lsysCollection = list()     # Colleciton of lsys objects currently loaded

    # Intro to everything, check for loadable file
    print( "Hello. Welcome to lsys." )
    if( len(sys.argv) == 2 ):
        filename = sys.argv[1]
        try:
            f = open( filename )
            lsysCollection = getLsysFromFile( filename )
            print( "Sucessfully loaded: {}. ".format(filename) )

        except FileNotFoundError:
            print( "Could not open file: {}".format(filename) )
    else:
        print( "No file was loaded. Use 'load [filename]' to parse a file for lsys objects." )

    # Main loop
    while True:

        # Prompt, extract command term and params
        userIN = input( ">" ).strip(" ")
        cmdTerm = userIN.split(" ")[0].lower()
        if( len(userIN.split(" ")) >= 2 ):
            param = userIN.split(" ")[1]
        else:
            param = None

        #print("Got tokens: {}".format(userIN.split(" ")))

        # Determine what should be done w/ the command term and param
        if cmdTerm == 'l' or cmdTerm == 'load':
            if param == None:
                print( "Invalid use of 'load'. Usage \'load [filename]\'" )
                continue

            try:
                lsysCollection += getLsysFromFile( param )
                print("Sucessfully loaded: {}. ".format(filename))
            except FileNotFoundError:
                print("Error: File was not found: {}".format(param) )
            except IndexError:
                print("Error: Invalid syntax in datafile.")

        elif cmdTerm == 'help' or cmdTerm == 'h':
            printHelp()

        elif cmdTerm == 'display' or cmdTerm == 'd':
            printCollection( lsysCollection )

        elif cmdTerm == 'size' or cmdTerm == 's':
            if not param.isdigit():
                print( "Invalid use of 'size'. Usage \'size [filename]\'" )
            else:
                size = int(param)
                print( "Size is now set to {}.".format(size) )

        elif cmdTerm == 'run' or cmdTerm == 'r':

            # This will store the lsys object
            obj = None

            # Allow user to select lsys by number
            if param.isdigit():
                obj = lsysCollection[ int(param) - 1 ]

            # Allow user to select lsys by name
            else:
                for l in lsysCollection:
                    if l.getName() == param:
                        obj = l

            # Check if object was found
            if obj == None:
                print("Could not find an lsys w/ name '{}'".format(param))

            else:
                print("Using an lsys called {}.".format(obj.getName()))

                try:
                    n = int(userIN.split(" ")[2])
                    # int(input("How many iterations should be performed? "))
                    turtleInit()
                    print("Generating image. This may or may not take a while.")

                    try:
                        runLsys( obj, n, size )
                        update()
                        toSave = input("Image Generated. Would you like to save it? (y/n) ").lower()
                        if toSave == "y":
                            ts = getscreen().getcanvas()
                            name = "{}_{}_{}.svg".format(obj.getName(), str(n), str( datetime.date.today() ))
                            canvasvg.saveall( name, ts)     # Save as svg
                            #ts.postscript(file=name)        # Save as eps (Does not save entire image)

                            print("Saved image w/ name: {}".format(name))
                        else:
                            print("Exited turtle w/o saving image. Done.")

                    except RecursionError:
                        print("A Stack Overflow occurred; try again w/ fewer iterations.")
                except ValueError:
                    print("Error: The number of iterations must be a non-negative integer. Aborting...")
                except IndexError:
                    print("Error: # of iterations not given. Usage: 'run [lsys_name/num] [#_of_iterations]'")


        elif cmdTerm == 'exit' or cmdTerm == 'quit' or cmdTerm == 'q':
            exit()

        else:
            print("Unknown command: {}".format(cmdTerm) )

if __name__ == "__main__":
    main()
