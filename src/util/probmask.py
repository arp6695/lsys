"""
Probability masks. Used for calculating non-uniform distributions.
Should work with floating-point numbers.

E.g. the probability mask:
"Hello" (0.50)
"World" (0.25)
"Asdfg" (0.25) 

Will roll "Hello" about 50% of the time, and the others about 25% each
"""
import random

SEED = 123456789

""" Helper class which uniquely maps an element to a probability of that element occurring. """
class Probability(object):
    def __init__(self, elem, prob):
        self.elem = elem
        self.prob = prob

class ProbabilityMask(object):

    """ Constructor """
    def __init__(self, elemlist=[], problist=[]):
        random.seed( SEED )
        self.mask = list()
        if len(elemlist) != len(problist): 
            raise AttributeError( f"Lengths of lists differ: {len(elemlist)} != {len(problist)}"  )

        for i in range(len(elemlist)):
            self.mask.append( Probability(elemlist[i], problist[i]) )
    
    """ Explicitly add an outcome and it's probability """
    def add(self, elem, prob):
        self.mask.append( (elem, prob) )

    """ Return whether this object is populated with values or not. """
    def isEmpty(self):
        return len(self.mask) == 0

    """ Check that the probabilities add up to 1. Unvalidated masks will not have correct probability distributions. """
    def validate(self):
        if self.isEmpty(): return False
        
        sum = 0
        for item in self.mask:
            sum += item[1]
        return sum == 1

    """ Return an outcome based on the probabilities in the mask """
    def roll(self):
        # Roll a random number, then compare where it falls in all the probabilities.
        roll = random.random()
        sum = 0
        for item in self.mask:
            sum += item[1]
            if sum >= roll: return item[0]
        return None

    """ Use print-friendly string rep """
    def __str__(self):
        return self.printable()

    """ Return a stdout-friendly version of the mask """
    def printable(self):
        result = str()
        for item in self.mask:
            result += f"{item[0]}: {item[1] * 100}%\n"
        return result

    """ Return a parser-friendly string representation """
    def asString(self):
        pass # TODO



