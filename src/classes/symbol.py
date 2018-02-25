"""
    symbol.py
    template for inevitable switch from informal string symbols to a formal
    object-oriented symbol definition when

    symbol params should map string variables to integer

    Also funcitons as a Parametric Module

    Fields
    token - A string token representing the symbol
    bools - A collection of boolean expressions, all of which must be
        evaluated true for the parametric to be considered true
    params - A map of string variable names to integer/float values

"""

class symbol(object):

    def __init__( self, token, bools=[], params=dict() ):
        self.token = token
        self.bools = bools
        self.params = params

    def evalBools( self ):

        # Variables must be cast from params before being evaluated
        for var in self.params.keys():
            exec( "{0} = {1}".format( var, self.params[var] ) )

        # Evaluate booleans
        for b in self.bools:
            if eval( b ):
                return False

        return True
