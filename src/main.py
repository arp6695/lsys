"""
Main frontend for lsys
Prompts for in-file, read and construct lsys objects
    Then prompt for # of iterations
    Draw, wait
Prompt to save the image (defaults to scalable vector img)
Goto 1

The alphabet has preset tokens that automatically correspond to turtle actions:
    'F' 'G' 'H' 'I' 'J' - Forward by a given unit (Draw)
    'f' 'g' 'h' 'i' 'j' - Forward by a given unit (Do not draw)
    'K' - Forward by a given unit (Does not Draw)
    'L' - Leaf - Forward, w/ two 'leaves'
    '+' - Left by the lsys' angle
    '-' - Rigth by the lsys' angle
    '[' - Push tuple w/ turtle position and angle onto stack
    ']' - Pop tuple w/ turtle position and angle off of stack, apply turtle position & angle
    '#' - Change the color of the pen; MUST be followed by a six digit hex string, which indicates the color
    Unlisted capital letters have no associated action (A, B, C, X, Y, Z are conevention).

Following commands are:
    'load [file]' or 'l [file]'                     -   Read and parse lsys objects from a given data file
    'display'                                       -   Print all currently loaded lsys objects
    'run [lsys_name]'                               -   Run recursions on a loaded lsys object, uses python's turtle
    'runthru [lsys_name] [first_itr] [final_itr]'   -   Run a sequence of recursions on a lsys object
    'mod [lsys_name] [lsys_attr] [new_attr_val]'    -   Modify a field of an lsys (angle or axiom)
    'dump'                                          -   Unload all currently loaded lsys objects
    'size [int]'                                    -   Change the size of the picture (5 by default)
    'help'                                          -   Print this help screen
    'exit' or 'quit'                                -   Quit the program
"""

import sys                  # For Command Line Arguments
import os                   # For determining the current directory (image saving & file loading)
import datetime             # For naming images
import turtle as t          # For Drawing TODO: Move this
from math import sqrt

from util.io import *       # For Reading/Writing lsys to/from files
from util.stack import *    # For Stack support

try:
    import canvasvg         # For saving images. This is a non-standard module, so report it if it cannot be opened.
except ImportError:
    print("Warning: Could not import 'canvasvg'. You will be unable to save images.")

# Global Stack (for saving turtle position and heading between recursive function calls)
STACK = Stack()

DEFAULT_COLOR_FILE = "src/misc/colors.xml"

DEFAULT_DATA_FILE = "src/data/all.xml"

try:
    COLORS = getColors( DEFAULT_COLOR_FILE )
except FileNotFoundError:
    COLORS = None
except ValueError:
    COLORS = None

def chooseAction( token, size, angle ):
    """ Determine which turtle action to use.
    
    Helper for recursive turtle implementation
    Args:
        token: A string, token from lsys alphabet
        size: An integer, the length the turtle will go forward
        angle: An integer, the angle associated with the lsys
    """
    global STACK

    # Defaults
    if token in "FGHIJ":
        t.forward( size )
    elif token in "fjhij":
        t.up()
        t.forward( size )
        t.down()
    elif token == "-":
        t.right( angle )
    elif token == "+":
        t.left( angle )

    # Stack related
    elif token == "[":
        STACK.push( tuple( [t.position(), t.heading()] ) )
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

def runLsys( lsys, depth, size ):
    """ Recursive function that recurses a given number of times, and determines turtle action.
    
    Args:
        lsys: An lsys object
        depth: Number of recursions
        size: Unit size of turtle
    Raises:
        RecursionError: If the maximum number of stack frame is exceeded.
    """

    # Clear stack, failsafe against unbalanced lsys
    global STACK
    if not STACK.isEmpty():
        STACK = Stack()

    t.setup()
    t.tracer(False) # Refresh the drawing manually, must use turtle.update() at the end
    t.hideturtle()
    t.setworldcoordinates( -300, -300, 300, 300 ) # NOTE: This may cause problems on different resolutions
    t.reset()

    print("The image is being generated. This may or may not take a while.")

    try:
        runLsysHelper( lsys.axiom, lsys, depth, size )
        t.hideturtle()
        t.update()
        print("Image generated. Use 'save' command to save the image to file.")

    except RecursionError:
        print("A Stack Overflow Error occurred; try again w/ fewer iterations.")

def runLsysHelper( string, lsys, depth, size ):
    """ Recursive Helper for 'runLsys'
    
    Args:
        string: A string to which the rules will be applied
        lsys: An lsys object
        depth: Number of recursions
        size: Unit size of turtle
    """

    global COLORS

    size_multiplier = 1

    for i in range(len(string)):
        char = string[i]

        if char == "#":
            id = ""
            i += 1
            while string[i].isdigit():
                id += string[i]
                i += 1
            try:
                t.color( COLORS[ int(id) ] )

            # No/invalid color file? Who cares?
            except t.TurtleGraphicsError:
                pass
            except TypeError:
                pass


        # Modify size multiplier by reading remaining string
        elif char == "@":
            s = ""
            i += 1

            while string[i].upper() in "1234567890.QI":
                s += string[i]
                i += 1

            if s[0].upper() == "Q":
                size_multiplier = sqrt( float(s[1:]) )
            elif s[0].upper() == "I":
                size_multiplier = 1 / float(s[1:])
            else:
                size_multiplier = float( s[0:] )

        # Character must correspond to some executable action
        elif depth <= 0 or char not in lsys.getVars():
            chooseAction( char, size * size_multiplier, lsys.angle )

        # Otherwise recurse with a rule string
        else:
            s = lsys.getResult( char, string[i-1] if i > 0 else "", string[i+1] if i < len(string)-1 else "" )
            runLsysHelper( s, lsys, depth-1, size * size_multiplier )

def printHelp():
    """ Print Help: read help.txt """
    for line in open( os.path.join( os.path.dirname(__file__), "misc/help.txt" )):
        print(line, end="")

def loadLsysFromFile( filename ):
    """ Return an lsys collection gotten from a parsed filename.
    Checks for errors and prints error messages.

    Args:
        filename: The file that the program will attempt to use to load L-Systems into memory.
    Returns:
        List of L-System objects.
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
    """ Find an L-System object given some user input.

    Args:
        lst: List of L-System to search through.
        param: User input parameter used to match one of the L-Systems.
    Returns:
        An L-System object that is 'matched' by the parameter.
    """
    obj = None

    if param.isdigit():     # Allow user to select lsys by number in collection
        try:
            obj = lst[ int(param) - 1 ]
        except IndexError:
            obj = None

    else:                   # Allow user to select lsys by name
        for l in lst:
            if l.name.lower() == param.lower():
                obj = l
    return obj

def display( param, lst ):
    if param == None:
        if len(lst) == 0:
            print("No lsys objects have been loaded.")
        else:
            print("Currently loaded objects are:")
            for i in range(len(lst)):
                print( "{}. {}".format( str(i+1), lst[i].name) )
    else:
        l = getLsysFromCollection( lst, param )
        if l == None:
            print("No such lsys object is loaded.")
        else:
            print( l )

def main():
    """ Primary Execution Loop. """
    size = 5

    global COLORS

    # Initialization: check for loadable file
    print( "Hello. Welcome to lsys." )
    if( len(sys.argv) >= 2 ):
        filename = sys.argv[1]
        # NOTE: command line filename will be relative to shell, not file
        lsysCollection = loadLsysFromFile( filename )
    else:
        lsysCollection = []
        try:
            lsysCollection = loadLsysFromFile( DEFAULT_DATA_FILE )
        except FileNotFoundError:
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

        if 'help'.startswith( cmdTerm ):
            printHelp()

        if 'colors'.startswith( cmdTerm ):
            if COLORS == None:
                print("No colors are loaded.")
            else:
                print( COLORS )

        elif 'display'.startswith( cmdTerm ):
            display( param, lsysCollection )

        elif 'size'.startswith( cmdTerm ):
            if not param.isdigit():
                print( "Invalid use of 'size'. Usage \'size [int]\'" )
            else:
                size = int(param)
                print( "Size has been set to {}.".format(size) )

        elif 'run'.startswith( cmdTerm ):

            obj = getLsysFromCollection( lsysCollection, param )

            if obj == None:         # Check if object was found
                print("Could not find an lsys w/ name/number '{}'".format(param))

            else:
                print("Using the lsys called {}.".format(obj.name))

                try:
                    n = int(userIN[2])
                    runLsys( obj, n, size )

                except ValueError:
                    print("Error: The number of iterations must be a non-negative integer. Aborting...")
                except IndexError:
                    print("Error: # of iterations not given. Usage: 'run [lsys_name/num] [#_of_iterations]'")
                except t.Terminator:
                    # NOTE Don't touch this; program will crash on closing turtle window NOTE
                    # Fuck it, run it again - it seems to work
                    runLsys( obj, n, size )

        elif 'runthru'.startswith( cmdTerm ):
            obj = getLsysFromCollection( lsysCollection, param )

            if obj == None:         # Check if object was found
                print("Could not find an lsys w/ name/number '{}'".format(param))

            else:
                print("Using the lsys called {}.".format(obj.name))
                try:
                    for i in range( int(userIN[2]), int(userIN[3]) ):
                        runLsys( obj, i, size )
                        if input("ENTER to continue. 'X' to quit.").upper() == "X":
                            break

                except ValueError:
                    print("Error: Invalid params for runthru range. Params must be integers.")

        elif 'save'.startswith( cmdTerm ):
            try:
                ts = t.getscreen().getcanvas()
                dir = os.path.dirname(__file__)
                filename = "images/{}_{}_{}.svg".format(obj.name, str(n), str( datetime.date.today()))

                canvasvg.saveall( os.path.join( dir, filename ), ts)     # Save as svg
            except NameError:
                print("The canvasvg module was not imported. You must install it to save images. \
                    Run 'pip install canvasvg'")
            except t.Terminator:
                print("The turtle canvas must be open to save the image. You must re-run your command to save.")

        elif 'load'.startswith( cmdTerm ):
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

        elif 'exit'.startswith( cmdTerm ) or 'quit'.startswith( cmdTerm ):
            exit()

        elif 'dump'.startswith( cmdTerm ):
            if "yes".startswith(input("Are you sure you'd like to dump currently loaded collection? (y/n) ").lower()):
                lsysCollection = list()
                print("Done.")

        elif 'mod'.startswith( cmdTerm ):
            l = getLsysFromCollection( lsysCollection, param )
            try:
                attr = userIN[2].lower()
                if attr == 'angle':
                    l.angle = ( float(userIN[3]) )
                elif attr == 'axiom':
                    l.axiom = ( userIN[3] )

                print("Set the {} of {} to be {}".format( attr, l.name, userIN[3] ))
            except ValueError:
                print("Error: Invalid attribute. Attribute must be float for angle.")
            except IndexError:
                print("Error: Invalid number of arguments. Usage 'mod [lsys_name] [lsys_attr] [new_attr_val]'")
            except AttributeError:
                print("Error: No lsys objects are currently loaded.")

        elif cmdTerm == '':
            pass

        else:
            print("Unknown command: {}".format(cmdTerm) )

if __name__ == "__main__":
    main()
