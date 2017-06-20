"""
IO Class
Read and write lsys objects to a plaintext file.
By: Alex Piazza

Lsys objects are written and read to a file like such:

    - Objects are seperated by semicolon, and encapsulated by braces
        { ... };

    - Object fields seperated commas, encapsulated by brackets
        { (), (), (), () };

    - Field 1: Alphabet tokens seperated by commas
        [A1, A2, A3, ... An]

    - Field 2: Starting string, NOT SEPERATED BY SPACES, nor commas
        [ ABC...n ]

    - Field 3: Rules, Different rules seperated by commas:
        [ (), (), ... () ]
        Rule are of this form: (AlphabetToken '->' NewString)
        Parenthesis are not necessary
        ( A -> ABC...n ),

    - Field 4: Integer Angle (still in braces)
        [n]

    - Field 5: String name (In braces, no quotes)
        [name_goes_here]

    Generic Form:
    { [A1, A2, A3, ... An], [ ABC...n ], [( A1 -> B1B2B3... ), ( A2 -> C1C2C3... ) ... ], [n], [str] };

    Sample:
    { [ A, B, C ], [ ABC ], [( A -> ABA ), ( B -> CAC )], [90], [HelloWorld] };

"""

from lsys import *

def getLsysFromString( string ):
    """
    Param 'string' is a string of the form: '{ [A, B, ...] ... [name_here] };'
    Return an lsys object
    Helper Function for getFromFile
    """
    result = createLsys()

    print("Parsing the string:" + string)

    # Remove '{', '}', ';' and ' ' (space) from the ends of the string
    # Split string by ']'
    tokens = string.strip("\{\}; ").replace(" ", "").split(")")
    for i in range( len(tokens) ):
        tokens[i] = tokens[i].strip(",(")

    #print( "tokens:" + str(tokens) )

    # Parse the ruleset
    ruleset = dict()
    for rule in tokens[2].split(","):
        # a 'rule' is of the form 'ABC->DEF'
        fromStr = rule.split("->")[0]
        toStr = rule.split("->")[1]
        ruleset[fromStr] = toStr

    # Set all the fields of the lsys
    result.setAlphabet( tokens[0].split(",") )
    result.setAxiom( tokens[1] )
    result.setRuleset( ruleset )
    result.setAngle( int(tokens[3]) )
    result.setName( tokens[4] )

    #print("Parsed an lsys object:\n" + str(result) )
    return result

def getLsysFromFile( filename ):
    """ Open a file designated by 'filename' and return a colleciton lsys objects parsed from it. """

    result = []
    for line in open(filename):
        for string in line.split(";"):
            if not string.isspace():
                result.append( getLsysFromString( string ) )
    return result

def writeToFile( filename, lst ):
    """ Write the given list 'lst' to a file w/ the given 'filename'. Overwrites contents of file. """
    # TODO
    pass
