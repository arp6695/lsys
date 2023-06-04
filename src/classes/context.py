"""
    context.py
    By: Alex Piazza
    Encapsulate two string symbols, left and right contexts
    Used to support context-sensitive grammars.
"""

class context(object):

    def __init__(self, left, right):
        """ Constructor.  """
        assert isinstance(left, str)
        assert isinstance(right, str)

        self.right = right
        self.left = left

def getContext():
    return context("/*", "/*")
