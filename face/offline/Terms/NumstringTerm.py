import offline.Terms.Term as Term
import random

class NumstringTerm(Term.BaseTerm):
	def execute(self, params):
		length = int(params[0])

		digits = [str(random.randint(0, 9)) for i in xrange(length)]			
		
		return (''.join(digits), ''.join(digits))
