"""
    Rule class definition
    rule.py
    By Alex Piazza

    The different kinds of rules are what make L-Systems as complex as they are.
    'Rules' generally describe the way a variable is transformed into a string of variables per iteraion.
    There are many ways that a variable can be mapped to resultant strings, a few ways are described below.

- Deterministically -
    This is the most strightforward: Each variable maps to a single result string which is always used to suppliment the
    variable during the transformation. Most of the already-implemented L-Systems in all.xml are deterministic.
    These are called 'deterministic' because the result yielded by a variable is determined and never changes.
    Ex. 'A' -> 'ABC'

- Stochastically -
    This is a variation one the idea of a deterministic L-Systems. With this, a variable maps to more than one result
    string, and the result string that will be used is randomly chosed from one of the many results. Each result has a
    weighted probability associated with it, so that some results will be chosen more/less frequently than others.
    Ex. 'A' -> 'ABC' (30%)
        'A' -> 'CBA' (30%)
        'A' -> 'AAA' (40%)
    A Deterministic rule is represented Stochastically as if it maps a variable to one result string 100% of the time.
    Ex. 'A' -> 'ABC' (100%)


- Context-Sensitive -
:NOTE: This has yet to be implemented :NOTE:

    This is also an extension on Stochastic L-Systems. A variable will map to many result strings, but the result will
    be chosen depending on the variable's neighboring symbols. Consider the axiom 'ABC'. Given a rule for 'B', say
    'B' -> 'A' only if 'A < B > C' will map the variable 'B' to 'A' if, and only if, 'A' is a symbol to the left of 'B',
    and 'C' is a symbol to the right of 'B', otherwise 'B' implicitly maps to nothing.
    Ex. 'B' -> 'A' only if 'A < B > C'

- Parametrically -
:NOTE: This has yet to be implemented :NOTE:

    This is by far the most complex L-System grammar. In it, some variables can be assigned parameters. 'A' with
    parameters 'x' and 'y' would resemble 'A(x,y)'. The rules would then map variables with specific parameters to
    specific result strings, and increment the paramaters in some way. For example, given the axiom 'A(0,0)', there
    could be a rule:
    'A(x,y)': x % 2 == 0 -> 'A(x+2, y+2)', which would yield the following sequence of results:
        A(0,0)
        A(2,2)
        A(4,4)
        A(6,6), etc.


    In this implementation, a rule has 'productions', which map 'context' objects to 'cases' objects.
    Context objects encapsulate two string, which correspond to the left/right contexts of a given token.
    Cases objects encapsulate a list of result strings and it's respective probability mask.

"""

import re   # For matching context-sensitive tokens
from util.probmask import ProbabilityMask

DEFAULT_RESULT_STRING = ""

class Rule( object ):

    def __init__(self, token=str() ):
        """ Constructor. 

        Args:
            token: The token that this rule will transform.
        """
        assert isinstance( token, str )

        self.token = token
        self.mask = ProbabilityMask()

    def __repr__(self):
        """ String representation.

        Returns:
            A console-friendly string representation of a rule.
        """
        return f"{self.token} -> " + self.mask.asPrintString()

    def getResult(self, left_token="", right_token=""):
        """ Get the string output (result) associated with this rule 
        
        Args:
            left_token: The token to the left of this token. Context-sensitive grammars override this.
            right_token: The token to the right of this token. Context-sensitive grammars override this.
        Returns:
            The result of applying this rule to the token, relative to the adjacent tokens.
        """
        return self.mask.roll()
                        
    def isStochastic(self):
        """ Check whether this rule is stochastic or not.
        
        Returns:
            True if this rule has a properly populated probability mask. False otherwise
        """
        result = not self.mask.isEmpty()
        result &= len(self.mask) != 1       # Deterministic rules have only one outcome.
        return result

    def isContextSensitive(self):
        """ Check whether this rule is context-sensitive or not.
        
        Returns:
            True if this rule is context-sensitive. False otherwise.
        """
        # TODO
        return False
