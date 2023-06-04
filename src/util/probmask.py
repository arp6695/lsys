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

class Probability(object):
    """ Helper class which uniquely maps an element to a probability of that element occurring. """
    
    def __init__(self, elem, prob):
        """ Constructor
        Args:
            elem: The outcome of the rule, if it is applied.
            prob: The probability that this rule will be applied.
        """
        self.elem = elem
        self.prob = prob


class ProbabilityMask(object):
    def __init__(self, probList=[]):
        """ Constructor

        Args:
            probList: list of Probability objects.
        Returns:
            ProbabilityMask object.
        Raises:
            AttributeError: if probList contains a non-Probability object.
        """
        random.seed( SEED )
        self.mask = list()
        for prob in probList:
            if isinstance( prob, Probability ):
                self.mask.append( prob )
            else:
                raise AttributeError( f"Error: Probability list contains non-Probability object: {prob}"  )
    
    def add(self, elem, prob):
        """ Explicitly add an outcome and it's probability
        
        Args:
            elem: The outcome of the rule, if it is applied.
            prob: The probability that this rule will be applied.
        """
        self.mask.append( Probability(elem, prob) )

    def isEmpty(self):
        """ Return whether this object is populated with values or not. """
        return len(self.mask) == 0

    def validate(self):
        """ Check that this probability mask is valid.
        
        Returns:
            True if the probabilities add up to 1.
            False otherwise.
        """
        if self.isEmpty(): return False

        sum = 0
        for item in self.mask:
            sum += item.prob
        return sum == 1

    def roll(self):
        """ Return an outcome based on the probabilities in the mask.
        
        Returns:
            The outcome of this rule's transformation, according to the probability distribution.
        """
        roll = random.random()
        sum = 0
        for item in self.mask:
            sum += item.prob
            if sum >= roll: return item.elem
        return None

    def __str__(self):
        """ String representation of the ProbabilityMask
        
        Returns:
            A console-friendly string representation
        """
        return self.printable()

    def asPrintString(self):
        """ Printable string representation.

        Returns:
            A console-friendly string representation.
        """
        result = str()
        for item in self.mask:
            result += f"{item[0]}: {item[1] * 100}%\n"
        return result

    def asParseString(self):
        """ Serializable string representation.

        Returns:
            An XML-friendly string representation. """
        result = ""
        format = "<case prob=\"{0}\" result=\"{1}\">\n"
        for item in self.mask:
            result += format.format( item.prob, item.elem )




