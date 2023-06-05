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


NOTE: Unused?
"""

class symbol(object):

    def __init__( self, token, bools=[], params=dict() ):
        """ Constructor
        
        Args:
            token: The string token that uniquely identifies this symbol.
            bools: Boolean expressions that should be evaluated to true 
            params: Map of tokens that parameterize this symbol.
        """
        self.token = token
        self.bools = bools
        self.params = params

    def evalBools( self ):
        """ Evaluate this symbol's boolean expressions.

        Returns:
            True if all the boolean expressions evaluate to true.
        """

        # Variables must be cast from params before being evaluated
        for var in self.params.keys():
            exec( "{0} = {1}".format( var, self.params[var] ) )

        # Evaluate booleans
        for b in self.bools:
            if eval( b ):
                return False

        return True
