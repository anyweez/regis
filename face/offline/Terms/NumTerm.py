import offline.Terms.Term as Term
import offline.ParserTools.ParserTools as ParserTools
import random

class NumTerm(Term.BaseTerm):
	def execute(self, params):
		pt = ParserTools.ParserTools()
		
		low, high = pt.prepare_params(params)
		num = random.randint(int(low), int(high))

		return (num, num)
