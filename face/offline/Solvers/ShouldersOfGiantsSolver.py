import face.offline.Solvers.Solver as Solver

class ShouldersOfGiantsSolver(Solver.BaseSolver):
	# This is going to be REALLY inefficient for now.  I'll come back
	# when time allows.
	def correct(self, st, params):
		maxnum = int(st.prepare_params(params)['max'])

		start_at = maxnum
		divisible = False
		
		while not divisible:
			divisible = True
			for divisor in xrange(1, maxnum+1):
				if start_at % divisor != 0:
					divisible = False
					start_at += 1
					break
				
		return [(start_at, None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
