import offline.Solvers.Solver as Solver

class NumbersInNumbersSolver(Solver.BaseSolver):
	def correct(self, st, params):
		digits = st.prepare_params(params)['digits']

		highest = 0
		for i in xrange(len(digits)):
			current = int(digits[i])
			if i+4 < len(digits):
				for j in xrange(4):
					current += int(digits[i+j+1])
				
				if current > highest:
					highest = current
		
		return [(highest, None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
