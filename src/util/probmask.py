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

    def __init__(self, elemlist=[], problist=[]):
        """ Constructor, May be initialized using a list of elements and their respective probabilities. """
        random.seed( SEED )
        self.mask = list()
        if len(elemlist) != len(problist): 
            raise AttributeError( f"Lengths of lists differ: {len(elemlist)} != {len(problist)}"  )

        for i in range(len(elemlist)):
            self.mask.append( Probability(elemlist[i], problist[i]) )
    
    def add(self, elem, prob):
        """ Explicitly add an outcome and it's probability """
        self.mask.append( (elem, prob) )

    def isEmpty(self):
        """ Return whether this object is populated with values or not. """
        return len(self.mask) == 0

    def validate(self):
        """ Check that the probabilities add up to 1. Unvalidated masks will not have correct probability distributions. """
        if self.isEmpty(): return False

        sum = 0
        for item in self.mask:
            sum += item[1]
        return sum == 1

    def roll(self):
        """ Return an outcome based on the probabilities in the mask """
        roll = random.random()
        sum = 0
        for item in self.mask:
            sum += item[1]
            if sum >= roll: return item[0]
        return None

    def __str__(self):
        """ Use print-friendly string rep """
        return self.printable()

    """ Return a stdout-friendly version of the mask """
    def asPrintString(self):
        result = str()
        for item in self.mask:
            result += f"{item[0]}: {item[1] * 100}%\n"
        return result

    def asParseString(self):
        """ Return a parser-friendly string representation """
        result = ""
        format = "<case prob=\"{0}\" result=\"{1}\">\n"
        for item in self.mask:
            result += format.format( item.prob, item.elem )




