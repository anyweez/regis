import face.offline.Terms.Term as Term
import face.offline.ParserTools.ParserTools as ParserTools

import random

# 'mixset' is a term that can be used to randomly select
# a set from a file and scramble all of the elements in
# the set.  It has two arguments, one required and one
# optional.
#    mixset setfile.txt [setlength]
#
# setlength will be honored when possible.

class MixsetTerm(Term.BaseTerm):
    def execute(self, params):
        filename = params[0]
        size_limit = None
    
        if len(params) > 1:
            size_limit = int(params[1])

        pt = ParserTools.ParserTools()
        lines = pt.load_datafile(filename)
        sets = pt.make_sets(lines)

        # If there is a size limit, restrict the sets that
        # can be used as much as possible.
        if size_limit:
            sets = [s for s in sets if len(s) == size_limit]

            if len(sets) is 0:
                sets = [s for s in sets if len(s) >= size_limit]
                if len(sets) is 0:
                    sets = pt.make_sets(lines)

        # Randomly choose a set and shuffle it around.
        chosen = random.choice(sets)
        random.shuffle(chosen)

        # If we have a specific size limit that we need to
        # meet, chop some random elements off of the end.
        if size_limit and len(chosen) > size_limit:
            chosen = chosen[:size_limit]

        return (chosen, chosen)
