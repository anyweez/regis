import face.offline.Solvers.Solver as Solver

class FindingFactorsSolver(Solver.BaseSolver):
	def correct(self, st, params):
		params = st.prepare_params(params)

		first = int(params['first'])
		second = int(params['second'])

		running_sum = 0
		for num in xrange(1001):
			if num % first == 0 and num % second == 0:
				running_sum += num

		return [(running_sum, None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
