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
    axiom attributes are assumed to contain only recognized symbols.
        See docstring of main.py for valid symbols. Don't try your luck with non-Ascii chars.


For each rule, a certain number of cases (<case>) must be provided.
Each case represents a given outcome of a transformation, and includes within it the resultant transformed string
(<result>), and the probability of that case occuring. The probability should be a floating point number less than
or equal to 1. Deterministic l-systems (DragonCurve, KochSnowflake, etc.) will have a single case with a probability
of '1', as each variable maps directly to a single, unchanging resultant string. A natural consequence of this is
that the file will be quite verbose, but this verbosity is to accomodate probabalistic grammars, and, frankly, is
the best I could come up with at the time.

The probabilities (prob) of each case within a given rule are assumed to be 1, but can be specified to be
any float or fraction. Note: These floats / fractions should add up to 1. An error will be thrown by
numpy unless an lsys object is run under these conditions

Each rule is defined by the variable token that it transforms. Thus each rule has an attribute that identifies
this variable (var).

Note: If you'd like to map a variable to nothing, then the <result> tag must have at least a space character
between the tags.

Syntax is as such:
Generic root tag (named 'data'), then one tag for each lsys. Of the form:

<data>
    <lsys name="default_name" angle="90" axiom="ABC" >
        <rule var="A">
            <case prob="1/3" result="ABC" />
            <case prob="0.5" result="DEF" />

            ...

            <context left="A" right="B" >
                <case prob="1/3" result="GHI" />
                <case prob="0.5" result="JKL" />

                ...

            </context>

        </rule>

        ...

    </lsys>
</data>

Note: The string in the 'context' element should be another token or a
    regular expression (as recognized by Python's 're' module)
    The 'context' element can optionally encapsulate a collection of cases;
    all cases without encapsulating contexts are the default cases, this would
    be the same as a context tag with universal selectors ("/*") as the left
    and right contexts.

Note: Probabilities for probabalistic rules should be floats that add up to 1, but are not checked
"""

from classes.lsys import *              # For creating lsys objects
from classes.rule import *              # For creating Rule Objects
from classes.cases import *
from classes.context import *
from util.probmask import *

import xml.etree.ElementTree as ET      # For parsing XML files
import fractions                        # For interpreting fractions parsed from data

def getLsysFromFile( filename ):
    """ Open a file designated by 'filename' and return a colleciton lsys objects parsed from it. """

    root = ET.parse( filename ).getroot()

    result = []

    # Iterate thru all lsys objects in root
    for child in root:

        l = getEmptyLsys()
        ruleset = dict()


        # Iterate thru all lsys attributes
        for attr in child.attrib.keys():
            if attr == "name":
                l.name = child.attrib[attr]
            elif attr == "angle":
                l.angle = float( fractions.Fraction( child.attrib[attr] ) )
            elif attr == "axiom":
                l.axiom = child.attrib[attr]

        # Iterate thru all rules
        for rule in child:

            ruleObject = getRule()
            var = rule.attrib["var"]
            cases = getCases()

            # Field will be either 'case' or 'context'
            # 'case' will be assumed to be context-free
            # 'context' will
            for field in rule:

                if field.tag == "case":

                    # Assume Probability is '1' unless otherwise specified
                    try:
                        cases.probabilities.append( float( fractions.Fraction( field.attrib["prob"] ) ) )
                        ruleObject.mask.add( field.attrib["result"].replace(" ", ""), float( fractions.Fraction( field.attrib["prob"] ) ) ) 
                    except KeyError:
                        cases.probabilities.append( 1.0 )
                        ruleObject.mask.add( field.attrib["result"].replace(" ", ""), 1.0 ) 

                    cases.results.append( field.attrib["result"].replace(" ", "") )

                    # Assume context is not sensitive unless otherwise specified
                    try:
                        l.rightcontext = field.attrib["right"]
                    except KeyError:
                        l.rightcontext = "/*"
                    try:
                        l.leftcontext = field.attrib["left"]
                    except KeyError:
                        l.leftcontext = "/*"


                if field.tag == "context":
                    (context, case) = getContextAndCases( field )
                    ruleObject.productions[context] = case

            ruleObject.productions[getContext()] = cases
            ruleset[var] = ruleObject

        l.ruleset = ruleset
        result.append( l )
    return result

def getContextAndCases( context_node ):
    """ Helper function for getLsysFromFile
        context_node - Child from 'ElementTree' with the tag 'context'
        Returns a context/case tuple
    """
    context = getContext()
    cases = getCases()

    try:
        context.right = context_node.attrib["right"]
    except KeyError:
        context.right = "/*"
    try:
        context.left = context_node.attrib["left"]
    except KeyError:
        context.left = "/*"

    for case in context_node:
        try:
            cases.probabilities.append( float( fractions.Fraction( case.attrib["prob"] ) ) )
        except KeyError:
            cases.probabilities.append( 1.0 )

        cases.results.append( case.attrib["result"].replace(" ", "") )


    return (context, cases)

def getColors( filename ):
    """ Open colors.xml and make a map of color id's to color strings.
        A color string can be either the color name or a hex string:
            Hex string -> '#00ccff'     (include the octothorpe)
            Color Name -> 'Red'
    """

    root = ET.parse( filename ).getroot()

    result = dict()

    for child in root:
        if child.tag == "color":
            result[ int(child.attrib["id"]) ] = child.attrib["color"]

    return result
