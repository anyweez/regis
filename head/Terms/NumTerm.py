#import Term
import Terms.Term as Term
import random

class NumTerm(Term.BaseTerm):
	def execute(self, params):
		low = int(params[0])
		high = int(params[1])
		
		return (random.randint(low, high), 3)
