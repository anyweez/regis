import offline.Terms.Term as Term
import random

class EvenTerm(Term.BaseTerm):
	def execute(self, params):
		low = int(params[0])
		high = int(params[1])

		num = random.randint(low, high)
		
		return (num, num)
