"""
Lindenmeyer System (lsys) class definition.
By: Alex Piazza

Lessons courtesy of Wikipedia https://en.wikipedia.org/wiki/L-system
A Lindenmeyer system is a way of rewriting strings. The symbols within these strings
change according to rules, and, when interpreted as commands to be executed by a turtle,
produce fractal images. L-Systems have:

    An Alphabet:
        A collection of Symbols that, along with the ruleset, collectivly comprise the L-System

    An Angle:
        The default angle that the turtle should turn
        Expressed by an float value 0-360, interpreted as degrees
        NOTE: I've seen lsys' angles be expressed as a divisor of 360
            e.g. If the lsys angle = 6, then the angle which turtle will turn is 360/6 degrees, or 60 degrees
            In this implementation, the L-System's angle is the angle that the turtle will turn, both left and right.

    An Axiom: A symbol or string of symbols that represents the initial state of the system

    A Symbol is a string token, and are either:
        A Constant: symbol which is not mapped to any string by the ruleset, and is therefore never changed
        A Variable: symbol which is mapped to a resultant string of other symbols in some way.
        There's no hard and fast trait that defines a symbol as a constant or variable within this L-System alphabet.
        i.e. Symbols are constant or vary by convention; this distinction is not specified in this system.
        Implicitly, a constant is defined as a variable that maps only to itself.

    Ruleset: 'rules' describing how symbols change from iteration to iteration.
    Specficially, this will be represented by a dictionary with the following key/val pairs:
        <symbol, rule>
        Where 'symbol' is a variable symbol and 'rule' is a rule object (see rule.py):
"""

class Lsys( object ):


    def __init__( self, name, angle, axiom, ruleset ):
        """ Constructor
    
        Args:
            name: A string identifier representing this L-System.
            angle: The default angle that the turtle should turn.
            axiom: The default string that will be operated upon
            ruleset: The map of tokens to rules that transform those tokens.
        Raises:
            IOError: If any of the parameters are improperly typed.
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
        self.vars = []
        self.alphabet = self.genAlphabet()

    def __repr__( self ):
        """ Create and return the string representation of an lsys object.
        
        Return:
            Console-friendly string representation of an L-System.
        """
        result = "Name: {0}\nAngle: {1} degrees\nAlphabet: {2}\nAxiom: {3}\n{4}"

        rule_string = ""
        for var in self.ruleset.keys():
            rule = self.ruleset[var]
            for context in rule.productions.keys():
                left_context = ("" if context.left == "/*" else "{} < ".format(context.left))
                right_context = ("" if context.right == "/*" else " > {}".format(context.right))

                cases = rule.productions[context]
                case_string = ""
                for i in range(len(cases.results)):
                    probability_string = "" if cases.probabilities[i] == 1 else "({}%) ".format(round(cases.probabilities[i] * 100, 2))
                    case_string += "{}{}; ".format( probability_string, cases.results[i])

                rule_string += "{0}{1}{2} -> {3}\n".format(left_context, var, right_context, case_string)


        if len(self.alphabet) == 0:
            self.alphabet = self.genAlphabet()

        alphabet_string = ""
        for sym in self.alphabet:
            alphabet_string += "{} ".format(sym)

        return result.format( self.name, self.angle, alphabet_string, self.axiom, rule_string )

    def getVars(self):
        """ Return every variable associated with this lsys. """
        if self.vars == []:
            for var in self.ruleset.keys():
                self.vars += var
        return self.vars

    def genAlphabet(self):
        """ Create and return the alphabet of this lsys.
        
        Returns:
            A list containing every symbol that this L-System could generate.
        """
        result = []
        for var in self.ruleset.keys():
            if var not in result:
                result.append(var)
            for context in self.ruleset[var].productions.keys():
                cases = self.ruleset[var].productions[context]
                for string in cases.results:
                    for symbol in string:
                        if symbol not in result:
                            result.append(symbol)
        return result

    def isComplete(self):
        """ Check if this L-System object has been populated compeltely and correctly.
        
        Returns:
            True if the lsys has valid and complete fields. False otherwise.
        """
        return len(self.name) > 0 and len(self.axiom) > 0 and len(self.ruleset) > 0 and self.angle is not 0

    def getResult( self, var, left_token, right_token ):
        """ Get the resultant string, given the right and left tokens

        Args:
            var: A variable symbol in this lsys' alphabet
            rotken: A symbol in the lsys' alphabet, to the right of 'var'
            ltoken: A symbol in the lsys' alphabet, to the left of 'var'
        """
        return self.ruleset[var].getResult( left_token, right_token )

def getEmptyLsys():
    """ Create and return an lsys with default params """
    return Lsys( str(), int(), str(), dict() )

