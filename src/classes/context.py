"""
    context.py
    By: Alex Piazza
    Encapsulate two string symbols, left and right contexts
    Used to support context-sensitive grammars.
"""

class Context(object):

    def __init__(self, left="/*", right="/*"):
        """ Constructor.
        
        Args:
            left: The left token.
            right: The right token.
        """
        assert isinstance(left, str)
        assert isinstance(right, str)

        self.right = right
        self.left = left

