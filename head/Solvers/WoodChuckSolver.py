import Solvers.Solver as Solver

class WoodChuckSolver(Solver.BaseSolver):
	def correct(self, params):
		return [(5, 'That is correct!'),]
		
	def mistakes(self, params):
		return [(3, 'Try a little higher'), (12, 'Nope, lower.')]
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
