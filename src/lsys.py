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

"""

class lsys( object ):
    """
    An 'lsys' object represents and L-System.
    It has:
        An Alphabet, of constants and variables
        An Axiom
        A Ruleset
        An angle (optional)
    (See above docstring for more details.)
    """

    def __init__( self, alphabet, axiom, ruleset, name, angle=0 ):
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

        if not isinstance(angle, int):
            raise IOError("Angle must be an integer")

        if not isinstance(name, str):
            raise IOError("Name must be a string")

        self.alphabet = alphabet
        self.axiom = axiom
        self.ruleset = ruleset
        self.angle = angle
        self.name = name

    def __repr__( self ):
        """ Create and return the string representation of an lsys object """
        result = "Name: {0}\nAlphabet: {1}\nAxiom: {2}\nRules: {3}\nAngle: {4} degrees\n"
        return result.format( self.name, self.alphabet, self.axiom, self.ruleset, self.angle )

    def to_CSV_String( self ):
        """ Return String representation of self (file writeable) """

        alphabetSTR = "[{}]".format( str(self.alphabet).replace( "\'", "" ))
        axiomSTR = "[{}]".format( self.axiom )
        angleSTR = "[{}]".format( self.angle )

        rulesetSTR = ""
        for key in self.ruleset.keys():
            rulesetSTR += "({} -> {})".format( key, self.ruleset[key] )
        rulesetSTR = "[{}]".format( rulesetSTR )

        return "\{ {0}, {1}, {2}, {3} \};".format( alphabetSTR, axiomSTR, rulesetSTR, angleSTR )

    ## Getters & Setters ##

    def addRule( old, new ):
        """ Add a rule to the lsys ruleset """
        assert old not in self.ruleset.keys()
        self.ruleset[old] = new

    def setAngle( angle ):
        assert isinstance( angle, int )
        self.angle = angle

    def setAlphabet( alphabet ):
        assert isinstance( lst, list )
        self.alphabet = alphabet

    def setAxiom( axiom ):
        assert isinstance( axiom, str )
        self.axiom = axiom

    def getName():
        return self.name

    def getAngle():
        return self.angle

    def getAxiom():
        return self.axiom

    def getAlphabet():
        # TODO 'import copy' and return a deepcopy instead
        return self.alphabet

    def getRuleset():
        # TODO 'import copy' and return a deepcopy instead
        return self.ruleset

def createLsys():
    """ Create and return an lsys with default params """
    return lsys( list(), str(), dict(), 0 )

def genStringItr( l, n ):
    """
    Generate a symbol string that can be read and interpreted as turtle commands
    Iterative
    """

    if not isinstance( l, lsys ):
        raise IOError( "'l' param not lsys object" )
    if not isinstance( n, int ) or n < 0:
        raise IOError( "'n' param not positive integer" )

    string = l.getAxiom()
    result = string
    for i in range(0,n):
        for char in string:
            result += l.getRuleset()[char]
        string = result
    return result
