import offline.Terms.Term as Term
import offline.ParserTools.ParserTools as ParserTools
import util.exceptions as exceptions

import random

class ChoosestrTerm(Term.BaseTerm):
    def execute(self, params):
        filename = params[0]
        size_limit = None
    
        if len(params) > 1:
            size_limit = int(params[1])

        pt = ParserTools.ParserTools()
        lines = pt.load_datafile(filename)

        line = random.choice(lines).strip()
        while len(line) is 0:
            line = random.choice(lines).strip()

        return (line, line)
