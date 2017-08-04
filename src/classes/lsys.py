"""
Lindenmeyer System (lsys) class definition.
By: Alex Piazza

Lessons courtesy of Wikipedia https://en.wikipedia.org/wiki/L-system
A Lindenmeyer system is a way of rewriting strings. The symbols within these strings
change according to rules, and, when interpreted as commands to be executed by a turtle,
produce fractal pictures.

    An Alphabet:
        A collection of symbols that, with the ruleset, collectivly comprise the L-System

    An Angle:
        The default angle that the turtle should turn
        Expressed by an float value 0-360, interpreted as degrees
        NOTE: I've seen lsys' angles be expressed as a divisor of 360
            e.g. If the lsys angle = 6, then the angle which turtle will turn is 360/6 degrees, or 60 degrees

    A Symbol is a string token, and are either:
        A Constant: symbol which is not mapped to any string by the ruleset, and is therefore never changed once created
        A Variable: symbol which is mapped to a
        There's no hard and fast trait that defines these within this L-System alphabet.
        Symbols are constant or vary by convention; this distinction is not specified in this system.

    An Axiom: A symbol or string of symbols that represents the initial state of the system

    Ruleset: 'rules' describing how symbols change from iteration to iteration.
    Specficially, this will be represented by a dictionary with the following key/val pairs:
        <symbol, tuple>
        Where 'symbol' is a variable symbol and 'tuple' is a tuple of two lists:
            the first list is a collection of every result string to which a given variable can map
            the second list contains the weighted probabilities of each string
                (ordering of this list corresponds to each variable in the previous list)
"""

class lsys( object ):
    """
    An 'lsys' object represents and L-System.
    It has:
        A Name
        An Angle
        An Axiom
        A Ruleset
        An Alphabet, of constants and variables
    """

    def __init__( self, name, angle, axiom, ruleset ):
        """
        Constructor for the lsys object
        """

        if not isinstance(axiom, str):
            raise IOError("Axiom must be a string.")

        if not isinstance(ruleset, dict):
            raise IOError("Ruleset must be a dictionary.")

        if not isinstance(angle, float) and not isinstance(angle, int):
            raise IOError("Angle must be an float")

        if not isinstance(name, str):
            raise IOError("Name must be a string")

        self.name = name
        self.angle = angle
        self.axiom = axiom
        self.ruleset = ruleset
        self.alphabet = self.genAlphabet()

    def __repr__( self ):
        """ Create and return the string representation of an lsys object """
        result = "Name: {0}\nAngle: {1} degrees\nAlphabet: {2}\nAxiom: {3}\nRules:\n{4}"

        rule_string = ""
        for key in self.ruleset.keys():
            rule = self.ruleset[key]

            if len(rule[0]) > 1:
                trans = ""
                for i in range(len(rule[0])):
                    trans += "\t({}%) {}\n".format( round(rule[1][i] * 100, 2), rule[0][i] )
            else:
                trans = "{}\n".format( rule[0][0] )
            rule_string += " {} -> {}".format(key, trans)

        if len(self.alphabet) == 0:
            self.alphabet = self.genAlphabet()

        alphabet_string = ""
        for sym in self.alphabet:
            alphabet_string += "{} ".format(sym)

        return result.format( self.name, self.angle, alphabet_string, self.axiom, rule_string )

    def genAlphabet(self):
        """ Create and return the alphabet of this lsys"""
        result = []
        for key in self.ruleset.keys():
            if key not in result:
                result.append(key)
            for string in self.ruleset[key][0]:
                for token in string:
                    if token not in result:
                        result.append(token)
        return result

    def isComplete(self):
        """ Returns True if the lsys has valid and complete fields """
        return len(self.name) > 0 and len(self.axiom) > 0 and len(self.ruleset) > 0 and self.angle is not 0

    def isStochastic(self):
        for var in self.ruleset.keys():
            if len(self.ruleset[var][0]) > 1:
                return True
        return False

    def isContextSensitive(self):
        return False

def createLsys():
    """ Create and return an lsys with default params """
    return lsys( str(), int(), str(), dict() )

def genStringIter( l, n ):
    """
    Generate a symbol string that can be read and interpreted as turtle commands
    Iterative, see main.py for the recursive version, entitled: 'runLsys'
    Takes a long time
    """

    if not isinstance( l, lsys ):
        raise IOError( "'l' param not lsys object" )
    if not isinstance( n, int ) or n < 0:
        raise IOError( "'n' param not positive integer" )

    string = l.getAxiom()
    result = string
    for i in range( n ):
        for char in string:
            result += l.getRuleset()[char]
        string = result
    return result

def genStringRec( l, n ):
    """ Returns a string using recursion """
    return genStringRecHelper( l, l.axiom, n )

def genStringRecHelper( l, s, n ):

    result = ""

    for char in s:
        if n <= 0 or char not in l.ruleset.keys():
            result += char
        else:
            result += genStringRecHelper( l, l.ruleset( char ), n-1 )
    return result
