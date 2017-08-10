"""
    case.py
    By Alex Piazza


    Presedence of Context-Sensitive Grammar with respect to Stochastics
    Context-Sensitive Grammar should superscede Stochastics. Meaning,
    a context-sensitive rule's output could be a determined stochastically,
    given that the context is/not satisfied, but a stochastic outcome cannot
    map to results that are determined by context.

"""

class case( object ):

    def __init__(self, results, probabilities, contexts):
        assert isinstance(results, list)
        assert isinstance(probabilities, list)
        assert isinstance(contexts, list)

        # Check the contents of non-empty lists
        try:
            assert isinstance(self.contexts[0], context)
        except IndexError:
            pass

        try:
            assert isinstance( self.probabilities[0], float )
        except IndexError:
            pass

        try:
            assert isinstance( self.results[0], str )
        except IndexError:
            pass

        self.results = results
        self.probabilities = probabilities
        self.contexts = contexts

def getCase():
    return case( list(), list(), list() )
