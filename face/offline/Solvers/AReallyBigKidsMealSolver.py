import offline.Solvers.Solver as Solver

class AReallyBigKidsMealSolver(Solver.BaseSolver):
	def mcnugget(self, num):
		if num is 0:
			return True
		elif num < 0:
			return False
		else:
			return (self.mcnugget(num-6) or self.mcnugget(num-9) or self.mcnugget(num-20))

	def correct(self, st, params):
		p = st.prepare_params(params)

		numbers = [p['a'], p['b'], p['c'], p['d'], p['e'], p['f'], p['g'], p['h'], p['i'], p['j']]
		mcnugs = [x for x in numbers if self.mcnugget(int(x))]
		
		return [(len(mcnugs), None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
