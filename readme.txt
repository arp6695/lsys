Turtle.tracer can be used to accel animation
Redo layout of lsys
Program for file i/o
	Read from file, Write object to file
	Standardize read/write format { [Alphabet], "axiom", RULESET }
Program for Stack
	pop, push, peek, isEmpty, etc.
Program for constructing lsys, standardized movement for turtle (F for forward, 45 for right 45 degrees, etc.)
	This need not be perfect, but consistant
	Possible implementation of a parser? 
		- Support function calls and params ( ?? -> turtle.right(45) )
		- Support stack ( ?? -> Stack.push( <symbol> ) )
		- Abstract segment size for scaleable pictures ( ?? -> turtle.forward( <symbol> ) ) (
		- Symbol Table ??
	convert string to python code? (w/o stding b/c code should not be run)
	Or hardcode map of strings to function calls
Multithreading for simultaneous construction of complete lsys string and turtle drawing.
Multithreading should be modeled as such: Recursive floor reached -> yield; Draw first string sequence; Recurse again - yield, etc. etc.
	This might need to change based on the nature of the recursion.
	Recursive structor should be modeled; redone
