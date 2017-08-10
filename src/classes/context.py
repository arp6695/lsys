"""
    context.py
    By: Alex Piazza
"""

class context(object):

    def __init__(self, default, left, right):
        """
        Create a new context object
            default - the string that will be selected by default, should the context not be met
            left - the symbol that should appear to the left of the variable to satisfy the context
            right - the symbol that should appear to the right of the variable to satisfy the context
        """

        assert isinstance( defualt, str )
        assert isinstance( left, str )
        assert isinstance( right, str )

        self.default = default
        self.left = left
        self.right = right

def createContext():
    return context( "/*", "/*" )
