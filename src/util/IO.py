"""
IO Class
Read and write lsys objects to a plaintext file.
By: Alex Piazza

Lsys objects are written and read to a file like such:

    - Objects are seperated by semicolon, and encapsulated by braces
        { ... };

    - Object fields seperated commas
        { (), (), (), () };

    { name, angle, axiom, rule1->newString1, rule2->newString2, ... ruleN->newStringN };

    TODO :
        Scostic Parsing: A( %50 )->ABA ; A( %50 )->BAB
        Color Parsing: A->(abc123)FAB
            (characters must be lowercase, and parenthesised ???)

"""

from lsys import *

def getLsysFromString( string ):
    """
    Param 'string' is a string of the form: '{ [A, B, ...] ... [name_here] };'
    Return an lsys object
    Helper Function for getFromFile
    """
    result = createLsys()
    ruleset = dict()


    # Remove '{', '}', ';' and ' ' (space) from the ends of the string
    # Split string by comma
    tokens = string.strip("\{\} ").split(",")

    #print("Split the line {} into tokens {}".format(string, tokens))

    # Parse rules here
    for i in range(3, len(tokens)):
        fromString = tokens[i].split("->")[0]
        toString = tokens[i].split("->")[1]
        ruleset[fromString] = toString

    # Set all the fields of the lsys
    result.setName( tokens[0] )
    result.setAngle( int(tokens[1]) )
    result.setAxiom( tokens[2] )
    result.setRuleset( ruleset )
    return result

def getLsysFromFile( filename ):
    """ Open a file designated by 'filename' and return a colleciton lsys objects parsed from it. """

    result = []
    for line in open(filename):
        for string in line.split(";"):
            string = string.replace(" ", "").replace("\t", "")
            try:
                if not string.isspace() and not string[0] == '#':
                    result.append( getLsysFromString( string ) )
            except IndexError:
                continue
    return result

def writeToFile( filename, lst ):
    """ Write the given list 'lst' to a file w/ the given 'filename'. Overwrites contents of file. """
    # TODO
    pass
