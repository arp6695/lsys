"""
IO Class
Read and write lsys objects to a plaintext file.
By: Alex Piazza

Lsys objects are written and read to a file like such:

    - Objects are seperated by semicolon, and encapsulated by braces
        { ... };

    - Object fields seperated commas, encapsulated by brackets
        { [], [], [], [] };

    - Field 1: Alphabet tokens seperated by commas
        [A1, A2, A3, ... An]

    - Field 2: Starting string, NOT SEPERATED BY SPACES, nor commas
        [ ABC...n ]

    - Field 3: Rules, Different rules seperated by commas, encapsulated in parenthesis:
        [ (), (), ... () ]
        Rule are of this form: (AlphabetToken '->' NewString)
        ( A -> ABC...n ),

    - Field 4: Integer Angle (still in braces)
        [n]

    Generic Form:
    { [A1, A2, A3, ... An], [ ABC...n ], [( A1 -> B1B2B3... ), ( A2 -> C1C2C3... ) ... ], [n] };

    Sample:
    { [ A, B, C ], [ ABC ], [( A -> ABA ), ( B -> CAC )], [90] };

"""

# TODO

def getFromFile( filename ):
    """ Open a file designated by 'filename' and return a colleciton lsys objects parsed from it. """
    # TODO
    pass

def writeToFile( filename, lst ):
    """ Write the given list 'lst' to a file w/ the given 'filename'. Overwrites contents of file. """
    # TODO
    pass
