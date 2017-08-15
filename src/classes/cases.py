"""
    cases.py
    By: Alex Piazza
    Encapsulate string results and respective probabilities
"""

class cases(object):

    def __init__(self, results, probabilities):

        assert isinstance(results, list)
        assert isinstance(probabilities, list)

        self.results = results
        self.probabilities = probabilities

def getCases():
    return cases( [], [] )
