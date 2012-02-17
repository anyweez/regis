import offline.Solvers.Solver as Solver

class OneOfAKindSolver(Solver.BaseSolver):
	def correct(self, st, params):
		nums = self.load_userfile()
		unique = list(set(nums))
		
		return [(len(unique), None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
