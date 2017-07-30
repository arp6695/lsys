"""
IO Class
Read lsys objects from a XML files.
By: Alex Piazza

New Storage using XML - For data file readability

The XML Tree for an l-system (lsys) object are virtually identical to the way the objects are constructed
with the slight exception of how the rule elements accomodate a probabalistic grammar.

Each lsys has attributes <name>, <angle>, and <axiom> tags which directly correspond to the name, angle and axiom
that will be fed into the internal representation of the lsys.

Notes:
    <axiom> tags are assumed to contain only recognized symbols.
        See docstring of main.py for valid symbols. Don't try your luck with non-Ascii chars.


For each rule, a certain number of cases (<case>) must be provided.
Each case represents a given outcome of a transformation, and includes within it the resultant transformed string
(<result>), and the probability of that case occuring. The probability should be a floating point number less than
or equal to 1. Deterministic l-systems (DragonCurve, KochSnowflake, etc.) will have a single case with a probability
of '1', as each variable maps directly to a single, unchanging resultant string. A natural consequence of this is
that the file will be quite verbose, but this verbosity is to accomodate probabalistic grammars, and, frankly, is
the best I could come up with at the time.

The probabilities (<prob>) of each case within a given rule are assumed to add up to 1, but there is no check in place
to ensure that this is the case.

Each rule is defined by the variable token that it transforms. Thus each rule has an attribute that identifies
this variable (<var>).

Note: If you'd like to map a variable to nothing, then the <result> tag must have at least a space character
between the tags.

Syntax is as such:
Generic root tag (named 'collection'), then one tag for each lsys. Of the form:

<data>

...

    <lsys>
        <name> STR </name>
        <angle> INT </angle>
        <axiom> STR </axiom>

        <rule>
            <var> VAR </var>
            <case>
                <prob> FLOAT </prob>
                <result> STR </result>
            </case>
            <case>

                ...

            </case>
        </rule>
        <rule>

            ...

        </rule>

        ...

    </lsys>

    ...

</data>

Note: Probabilities for probabalistic rules should be floats that add up to 1, but are not checked
        TODO: This could be checked easily
"""

from lsys import *                      # For creating lsys objects
import xml.etree.ElementTree as ET      # For parsing XML files
import fractions                        # For interpreting fractions parsed from data

def getLsysFromFile( filename ):
    """ Open a file designated by 'filename' and return a colleciton lsys objects parsed from it. """

    root = ET.parse( filename ).getroot()

    result = []

    # Iterate thru all lsys objects in root
    for child in root:

        l = createLsys()
        ruleset = dict()

        # Iterate thru all lsys data fields
        for lsys_field in child:
            if lsys_field.tag == "name":
                l.name = lsys_field.text.replace(" ", "")
            elif lsys_field.tag == "angle":
                    l.angle = float( fractions.Fraction( lsys_field.text ) )
            elif lsys_field.tag == "axiom":
                l.axiom = lsys_field.text.replace(" ", "")
            elif lsys_field.tag == "rule":
                value = ([],[])
                key = None      # Must be initialized

                # Iterate thru each field under rule
                for rule_field in lsys_field:
                    if rule_field.tag == "var":
                        key = rule_field.text.replace(" ", "")
                    elif rule_field.tag == "case":

                        # Iterate thru each field in a given case
                        for case_field in rule_field:
                            if case_field.tag == "prob":

                                value[1].append( float( fractions.Fraction( case_field.text ) ) )

                            elif case_field.tag == "result":
                                value[0].append( case_field.text.replace(" ", "") )
                ruleset[key] = value
            else:
                break
        l.ruleset = ruleset
        result.append( l )
    return result


### NOTE These functions are deprecated NOTE ###
### Use XML Format instead ###

def getLsysFromCSV( filename ):
    result = []
    for line in open(filename):
        for string in line.split(";"):
            string = string.replace(" ", "").replace("\t", "")
            try:
                if not string.isspace() and not string[0] == '#':
                    result.append( getLsysFromString( string ) )
            except IndexError:
                continue
    return result

def getLsysFromString( string ):
    """
    Param 'string' is a string of the form: '{ [A, B, ...] ... [name_here] };'
    Return an lsys object
    Helper Function for getFromFile
    """
    result = createLsys()
    ruleset = dict()


    # Remove '{', '}', ';' and ' ' (space) from the ends of the string
    # Split string by comma
    tokens = string.strip("\{\} ").split(",")

    # Parse rules here
    for i in range(3, len(tokens)):
        fromString = tokens[i].split("->")[0]
        toString = tokens[i].split("->")[1]
        ruleset[fromString] = toString

    # Set all the fields of the lsys
    result.name = tokens[0]
    result.angle = int(tokens[1])
    result.axiom = tokens[2]
    result.ruleset = ruleset
    print( "Got a result " + str(result) )
    return result
