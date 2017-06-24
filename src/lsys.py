"""
Lindenmeyer System (lsys) class definition.
By: Alex Piazza

Lessons courtesy of Wikipedia https://en.wikipedia.org/wiki/L-system
A Lindenmeyer system is a way of rewriting strings. The symbols within these strings
change according to rules, and, when interpreted as commands to be executed by a turtle,
produce fractal pictures.

    An Alphabet:
        A collection of symbols that, with the ruleset, collectivly comprise the L-System

    A Symbol is a string token, and are either:
        A Constant: symbol which is not mapped to any string by the ruleset, and is therefore never changed once created
        A Variable: symbol which is mapped to a
        There's no hard and fast trait that defines these within this L-System alphabet.
        Symbols are constant or vary by convention; this nature is not specified in this system.

    An Axiom: A symbol or string of symbols that represents the initial state of the system

    Ruleset: 'rules' describing how symbols change from iteration to iteration.
    Specficially, this will be represented by a dictionary with the following key/val pairs:
        <symbol, string>
        Where 'symbol' is a variable symbol and 'string' is a string of symbols, consisting of
        the variables and constants to replace 'symbol'.

    An Angle:
        The default angle that the turtle should turn
        Expressed by an integer value 0-360, interpreted as degrees
        NOTE: I've seen lsys' angles be expressed as a divisor of 360
            e.g. If the lsys angle = 6, then the angle which turtle will turn is 360/6 = 60 degrees

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

        if not isinstance(angle, int):
            raise IOError("Angle must be an integer")

        if not isinstance(name, str):
            raise IOError("Name must be a string")

        self.name = name
        self.angle = angle
        self.axiom = axiom
        self.ruleset = ruleset
        self.alphabet = genAlphabet()

    def __repr__( self ):
        """ Create and return the string representation of an lsys object """
        result = "Name: {0}\nAlphabet: {1}\nAxiom: {2}\nRules: {3}\nAngle: {4} degrees\n"
        return result.format( self.name, self.alphabet, self.axiom, self.ruleset, self.angle )

    def to_CSV_String( self ):
        """ Return String representation of self (file writeable) """

        #alphabetSTR = "({})".format( str(self.alphabet).replace( "\'", "" ))
        nameSTR = "({})".format( self.name )
        angleSTR = "({})".format( self.angle )
        axiomSTR = "({})".format( self.axiom )

        rulesetSTR = ""
        for key in self.ruleset.keys():
            rulesetSTR += "{}->{},".format( key, self.ruleset[key] )
        rulesetSTR = "({})".format( rulesetSTR ).rstrip(",")

        return "{ {0}, {1}, {2}, {3}, {4} };".format( nameSTR, angleSTR, axiomSTR, rulesetSTR )

    ## Getters & Setters ##

    def addRule( self, old, new ):
        """ Add a rule to the lsys ruleset """
        assert old not in self.ruleset.keys()
        self.ruleset[old] = new

    def setAngle( self, angle ):
        assert isinstance( angle, int )
        self.angle = angle

    def setAlphabet( self, alphabet ):
        assert isinstance( alphabet, list )
        self.alphabet = alphabet

    def setAxiom( self, axiom ):
        assert isinstance( axiom, str )
        self.axiom = axiom

    def setName( self, name ):
        self.name = name

    def setRuleset( self, ruleset ):
        self.ruleset = ruleset

    def getName(self):
        return self.name

    def getAngle(self):
        return self.angle

    def getAxiom(self):
        return self.axiom

    def getAlphabet(self):
        if len(self.alphabet) == 0:
            self.alphabet = self.genAlphabet()
        else:
            return self.alphabet

    def getRuleset(self):
        return self.ruleset

    def genAlphabet(self):
        """ Create and return the alphabet of this lsys"""
        result = []
        for key in self.ruleset.keys():
            if key not in result:
                result.append(key)
            for val in self.ruleset[key]:
                if val not in result:
                    result.append(val)
        return result

def createLsys():
    """ Create and return an lsys with default params """
    return lsys( "default_name", 0, str(), dict() )

def genString( l, n ):
    """
    Generate a symbol string that can be read and interpreted as turtle commands
    Iterative, see main.py for the recursive version, entitled: 'runLsys'
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
