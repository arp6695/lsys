"""
Stack functionality
Not efficient nor necessary, but a formal stack definition is used in lsys
By: Alex Piazza

Supports pushing, popping, & peeking
Uses tuples as underlying data encapsulation
    Tuples are of the form: ( some_data, referent_to_next )

"""

class Stack( object ):

    def __init__( self ):
        self.top = None

    def __repr__(self):
        """
            String representation:
            "data1 -> data2 -> data3 -> ... -> dataN -> None"
        """
        string = ""
        ptr = self.top
        while ptr != None:
            string += str(ptr[0]) + " -> "
            ptr = ptr[1]    # Set pointer to 'next'
        string += "None"
        return string

    def push( self, data ):
        """ Push new data onto the stack """
        newTop = ( data, self.top )
        self.top = newTop

    def pop( self ):
        """ Pop and return the top of the stack """
        assert not self.isEmpty()
        data = self.top[0]          # Get Data in tuple
        self.top = self.top[1]      # Set top to current top's 'next' reference
        return data

    def peek( self ):
        """ Return top of the stack w/o removing it. """
        if self.isEmpty():
            return None
        return self.top[0]

    def isEmpty( self ):
        """ True iff top is None -> Stack is empty"""
        return self.top == None

def getStack():
    return Stack()
