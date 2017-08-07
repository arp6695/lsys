"""
    rule.py
    By Alex Piazza
"""

import re

try:
    import numpy            # For choosing symbol string with weighted probabilities
except ImportError:
    print("Warning: Could not import 'numpy'. You will be unable to draw stochastic L-systems.")

class rule( object ):

    def __init__(self, var, cases, rcontext, lcontext):

        assert isinstance( var, str )
        assert isinstance( cases, tuple )
        assert isinstance( rcontext, str )
        assert isinstance( lcontext, str )

        self.var = var
        self.cases = cases
        self.rcontext = rcontext
        self.lcontext = lcontext

    def __repr__(self):
        result = "{} -> ".format( self.var )

        if len(cases[0]) > 1:
            for i in range(len(self.cases[0])):
                result += "\t({}%) {}\n".format( round(cases[1][i] * 100, 2) , cases[0][i] )
        else:
            result = "{} -> {}".format(self.var, self.cases[0][0])
        return result

    def getResult(self, ltoken, rtoken):
        """ Get the string output (result) associated with this rule """

        try:
            if (self.lcontext is "*" and self.rcontext is "*") or \
            (re.matches( rcon, self.rcontext ) and re.matches( lcon, lcontext )):
                return numpy.random.choice( self.cases[0], 1, True, self.cases[1] ).tolist()[0]
            else:
                return ""
        except NameError:
            return self.cases[0][0]
        except sre_constants.error:
            print("Error: Invalid regular expression")
            print("{}", self)

    def isContextSensitive(self):
        return self.rcontext != "*" and self.lcontext != "*"

def getRule():
    return rule( str(), tuple(), "*", "*" )
