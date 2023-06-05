"""
Stack functionality
Not efficient nor necessary, but a formal stack definition is used in lsys
By: Alex Piazza

Supports pushing, popping, & peeking
Uses tuples as underlying data encapsulation
    Tuples are of the form: ( some_data, reference_to_next_tuple )

"""

class Stack( object ):

    def __init__( self ):
        self.top = None

    def __repr__(self):
        """ String representation:

        Returns:
            A console-friendly string representation.
        """
        string = ""
        ptr = self.top
        while ptr != None:
            string += str(ptr[0]) + " -> "
            ptr = ptr[1]    # Set pointer to 'next'
        string += "None"
        return string

    def push( self, data ):
        """ Push data to the top of the stack.
        
        Args:
            data: New datum to put on the top of the stack.
        """
        newTop = ( data, self.top )
        self.top = newTop

    def pop( self ):
        """ Remove the topmost item and return it.
        
        Returns:
            The topmost datum.
        """
        assert not self.isEmpty()
        data = self.top[0]          # Get Data in tuple
        self.top = self.top[1]      # Set top to current top's 'next' reference
        return data

    def peek( self ):
        """ Peek at the top of the stack, without removing it.
        
        Returns:
            The topmost datum.
        """
        if self.isEmpty():
            return None
        return self.top[0]

    def isEmpty( self ):
        """ Check if the stack is empty or not.
        
        Returns:
            True if there is at least one data in the stack.
        """
        return self.top == None
