"""
Main frontend for lsys
Prompts for in-file, read and construct lsys objects
    Then prompt for # of iterations
    Draw, wait
Prompt to save the image (defaults to scalable vector img)
Goto 1

The alphabet has preset tokens that automatically correspond to turtle actions:
    'F' & 'G' - Forward by a given unit
    'L' - Leaf - Forward, w/ two 'leaves'
    '+' - Left by the lsys' angle
    '-' - Rigth by the lsys' angle
    '[' - Push tuple w/ turtle position and angle onto stack
    ']' - Pop tuple w/ turtle position and angle off of stack, apply turtle position & angle
    Unlisted capital letters have no associated action (A, B, C, X, Y, Z are conevention).

Following commands are:
    'load [file]' or 'l [file]'         -   Read and parse lsys objects from a given data file
                                            (example files exist in src/data/)
    'display'                           -   Print all currently loaded lsys objects
    'run [lsys_name]'                   -   Run recursions on a loaded lsys object, uses python's turtle
    'runthru [lsys_name] [first_itr] [final_itr]'   -   Run a sequence of recursions on a lsys object
    'mod [lsys_name] [lsys_attr] [new_attr_val]'    -   Temporarily change a field of an lsys, (angle, axiom, or name)
    'dump'                              -   Unload all currently loaded lsys objects
    'color [color_name]'                -   Change the color of the turtle's pen
    'size [int]'                        -   Change the size of the picture (3 by default)
    'help'                              -   Print this help screen
    'exit' or 'quit'                    -   Quit the program

TODO: Enable stochasticism (redo [slightly] the parsing, allow for variability)
"""

import sys                  # For Command Line Arguments
import os                   # For determining the current directory (image saving)
import datetime             # For naming images
import turtle as t          # For Drawing

from util.IO import *       # For Reading/Writing lsys to/from files
from util.Stack import *    # For Stack support

try:
    import canvasvg         # For saving images; NOTE: This is a non-standard module -> 'pip install canvasvg'
except ImportError:
    print("Error: Could not import canvasvg. You will be unable to save images. \
        Use 'pip install canvasvg' to intall the module.")

STACK = getStack()

def turtleInit():
    """ Initialize the turtle module """
    t.setup()
    t.tracer(False) # Refresh the drawing manually, must use turtle.update() at the end
    t.hideturtle()
    t.setworldcoordinates( -300, -300, 300, 300 ) # NOTE: This may cause problems on different resolutions
    t.reset()

def chooseAction( token, size, angle ):
    """
    Determine which turtle action to use.
    Helper for recursive turtle implementation
    token - a string, token from lsys alphabet
    size - an integer, the length the turtle will go forward
    angle - an integer, the angle associated with the lsys
    """
    global STACK

    # Defaults
    if token == "F" or token == "G":
        t.forward( size )
    elif token == "-":
        t.right( angle )
    elif token == "+":
        t.left( angle )

    # Stack related
    elif token == "[":
        data = tuple( [t.position(), t.heading()] )
        STACK.push( data )
    elif token == "]":
        tpl = STACK.pop()
        t.penup()
        t.setpos( tpl[0] )
        t.seth( tpl[1] )
        t.pendown()

    # Fractal Tree related
    elif token == "L":      # Draws a line segment 'leaf'
        t.forward(size)
        t.lt(45)
        t.forward(size/4)
        t.backward(size/4)
        t.rt(90)
        t.forward(size/4)
        t.backward(size/4)
        t.lt(45)

    return None

def runLsys( l, n, s ):
    """
    Recursive function that recurses a given number of times, and determines turtle action.
    l - an lsys object
    n - an integer, number of recursions
    s - an integer, unit size of turtle
    """

    turtleInit()
    print("The image is being generated. This may or may not take a while.")

    try:
        runLsysHelper( l.getAxiom(), l, n, s )
        t.hideturtle()
        t.update()
        print("Image generated. Use 'save' command to save the image to file.")

    except RecursionError:
        print("A Stack Overflow Error occurred; try again w/ fewer iterations.")
        return

def runLsysHelper( string, l, n, s ):
    """
    Recursive Helper for 'runLsys'
    string - a string to which the rules will be applied
    l - an lsys object
    n - an integer, number of recursions
    s - an integer, unit size of turtle
    """
    for char in string:
        if n <= 0 or char not in l.getRuleset().keys():
            chooseAction( char, s, l.getAngle() )
        else:
            runLsysHelper( l.transformRule( char ), l, n-1, s )
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
    for line in open( os.path.join( os.path.dirname(__file__), "/misc/help.txt" )):
        print(line, end="")

def loadLsysFromFile( filename ):
    """
    Return an lsys collection gotten from a parsed filename.
    Checks for errors and prints error messages.
    """
    lst = list()
    try:
        lst = getLsysFromFile( filename )
        print("Sucessfully loaded: {}. Use 'display' to see the updated list of lsys objects.".format( filename ))
        return lst
    except FileNotFoundError:
        print("Error: File was not found: {}".format( filename ) )
    except IndexError:
        print("Error: Invalid syntax in datafile.")
    except ValueError:
        print("Error: Invalid syntax in datafile.")
    return lst

def getLsysFromCollection( lst, param ):
    obj = None

    if param.isdigit():     # Allow user to select lsys by number in collection
        try:
            obj = lst[ int(param) - 1 ]
        except IndexError:
            obj = None

    else:                   # Allow user to select lsys by name
        for l in lsysCollection:
            if l.getName() == param:
                obj = l
    return obj

def main():
    size = 3
    color = "black"

    # Initialization: check for loadable file
    print( "Hello. Welcome to lsys." )
    if( len(sys.argv) >= 2 ):
        filename = sys.argv[1]
        # NOTE: command line filename will be relative to shell, not file
        lsysCollection = loadLsysFromFile( filename )
    else:
        lsysCollection = list()
        print( "No file was loaded. Use 'load [filename]' to parse a file for lsys objects." )

    # User input loop
    while True:

        # Prompt, extract command term and params
        userIN = input( "lsys>" ).lower().strip(" ").split(" ")
        cmdTerm = userIN[0]
        if( len(userIN) >= 2 ):
            param = userIN[1]
        else:
            param = None

        # Determine what should be done w/ the command term and param
        if cmdTerm == 'color' or cmdTerm == 'c':
            try:
                # NOTE: This doesnt work, dunno why
                t.color(param)
            except t.TurtleGraphicsError:
                print("Error: '{}' is not a valid color for the turtle.".format(param))

        elif cmdTerm == 'help' or cmdTerm == 'h':
            printHelp()

        elif cmdTerm == 'display' or cmdTerm == 'd':
            printCollection( lsysCollection )

        elif cmdTerm == 'size' or cmdTerm == 's':
            if not param.isdigit():
                print( "Invalid use of 'size'. Usage \'size [int]\'" )
            else:
                size = int(param)
                print( "Size has been set to {}.".format(size) )

        elif cmdTerm == 'run' or cmdTerm == 'r':

            obj = getLsysFromCollection( lsysCollection, param )

            if obj == None:         # Check if object was found
                print("Could not find an lsys w/ name/number '{}'".format(param))

            else:
                print("Using the lsys called {}.".format(obj.getName()))

                try:
                    n = int(userIN[2])
                    runLsys( obj, n, size )

                except ValueError:
                    print("Error: The number of iterations must be a non-negative integer. Aborting...")
                except IndexError:
                    print("Error: # of iterations not given. Usage: 'run [lsys_name/num] [#_of_iterations]'")
                except t.Terminator:
                    # NOTE: Turtle raises error if canvas is closed, dunno what the issue is
                    # Fuck it, do it again - it works
                    runLsys( obj, n, size )

        elif cmdTerm == 'runthru' or cmdTerm == 'rt':
            obj = getLsysFromCollection( lsysCollection, param )

            if obj == None:         # Check if object was found
                print("Could not find an lsys w/ name/number '{}'".format(param))

            else:
                print("Using the lsys called {}.".format(obj.getName()))
                try:
                    for i in range( int(userIN[2]), int(userIN[3]) ):
                        runLsys( obj, i, size )
                        if input("ENTER to continue. 'X' to quit.").upper() == "X":
                            break

                except ValueError:
                    print("Error: Invalid params for runthru range. Params must be integers.")

        elif cmdTerm == 'save' or cmdTerm == 's':
            try:
                ts = t.getscreen().getcanvas()
                dir = os.path.dirname(__file__)
                filename = "images/{}_{}_{}.svg".format(obj.getName(), str(n), str( datetime.date.today()))

                canvasvg.saveall( os.path.join( dir, filename ), ts)     # Save as svg
            except NameError:
                print("The canvasvg module was not imported. You must install it to save images. \
                    Run 'pip install canvasvg'")
            except t.Terminator:
                print("The turtle canvas must be open to save the image. You must re-run your command to save.")

        elif cmdTerm == 'load' or cmdTerm == 'l':
            if param == None:
                print( "Invalid use of 'load'. Usage \'load [filename]\'" )
            else:
                try:
                    lsysCollection += getLsysFromFile( param )
                    print("Sucessfully loaded: {}. \
                        Use 'display' to see the updated list of lsys objects.".format( param ))
                except FileNotFoundError:
                    print("Error: File was not found: {}.".format( param ) )
                except IndexError:
                    print("Error: Invalid syntax in datafile.")

        elif cmdTerm == 'exit' or cmdTerm == 'quit' or cmdTerm == 'q':
            exit()

        elif cmdTerm == 'dump':
            if input("Are you sure you'd like to dump currently loaded collection? (y/n) ").lower() == "y":
                lsysCollection = list()

        elif cmdTerm == 'mod' or cmdTerm == 'm':
            pass

        elif cmdTerm == '':
            pass

        else:
            print("Unknown command: {}".format(cmdTerm) )

if __name__ == "__main__":
    main()
