import offline.Terms.Term as Term
import offline.ParserTools.ParserTools as ParserTools
import util.exceptions as exceptions

import random

class ChoosesomeTerm(Term.BaseTerm):
    def execute(self, params):
        pt = ParserTools.ParserTools()
        filename, count = pt.prepare_params(params)
        lines = pt.load_datafile(filename)
        
        subset = random.sample([line.strip() for line in lines], int(count))
        return (subset, subset)
