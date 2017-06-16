"""
Lindenmeyer System (lsys) class definition.
By: Alex Piazza

Lessons courtesy of Wikipedia https://en.wikipedia.org/wiki/L-system
    An Alphabet:
        A collection of symbols, in no particular order

    A Symbol are string tokens, an are either:
        A Constant: symbol that cannot be removed by the ruleset, only added
        A Variable: symbol that can be changed by the ruleset
        There's no hard and fast trait that defines these within an lsys alphabet

    An Axiom: A symbol or string of symbols that represents the initial state of the system

    Ruleset: 'rules' describing how symbols change from iteration to iteration.
    Specficially, this will be represented by a dictionary with the following key/val pairs:
        <variable, string>
        Where 'variable' is a variable symbol and 'string' is a Python defined string of
        other variables and/or constants

    An Angle (Optional):
        The default angle that the turtle should turn; optional

    Each 'rule' in the list will be applied to the Axiom (or subsequent iteration) one
    after another. Therefore, the priority of the rules will be set by their respective
list indecies. Conflicting rules will be addressed in this way.

The alphabet has preset tokens that automatically correspond to turtle actions:
    'F' - Forward by a given unit (Variable)
    'G' - Forward by a given unit (Constant)
    '+' - Left by the lsys angle
    '-' - Rigth by the lsys angle
    '[' - Push tuple w/ turtle position and angle onto stack
    ']' - Pop tuple w/ turtle position and angle off of stack, reset turtle position & angle
    'X', 'Y', & 'Z' - Generic Constants - no action

"""

# TODO

class lsys( object ):
    """
    An 'lsys' object represents and L-System.
    It has:
        An Alphabet, of constants and variables
        An Axiom
        A Ruleset
    (See above docstring for more details.)
    """

    def __init__( self, alphabet, axiom, ruleset, angle=0 ):
        """
        Constructor for the lsys object
        """

        if not isinstance(alphabet, list):
            raise IOError("Alphabet must be a List of Strings")

        if not isinstance(axiom, str):
            raise IOError("Axiom must be a string.")
            if axiom not in alphabet:
                raise IOError("Axiom must be a part of the alphabet.")

        if not isinstance(ruleset, dict):
            raise IOError("Ruleset must be a dictionary.")

        self.alphabet = alphabet
        self.axiom = axiom
        self.ruleset = ruleset
        self.angle = angle

    def __repr__( self ):
        # TODO String representation of self (printable)

    def to_CSV_String( self ):
        # TODO String representation of self (file writeable)

def createLsys():
    """
    Create and return an lsys with default params
    """
    return lsys( list(), str(), dict(), 0 )
