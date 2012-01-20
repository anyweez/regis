import offline.Terms.Term as Term
import offline.ParserTools.ParserTools as ParserTools
import util.exceptions as exceptions

import random

# 'mixset' is a term that can be used to randomly select
# a set from a file and scramble all of the elements in
# the set.  It has two arguments, one required and one
# optional.
#    mixset setfile.txt [setlength]
#
# setlength will be honored when possible.

class ChoosesetTerm(Term.BaseTerm):
    def execute(self, params):
        filename = params[0]

        pt = ParserTools.ParserTools()
        lines = pt.load_datafile(filename)
        sets = pt.make_sets(lines)
        
        print len(sets)

        chosen = random.choice(sets)
        return (chosen, chosen)
