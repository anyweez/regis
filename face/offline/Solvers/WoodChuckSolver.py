import face.offline.Solvers.Solver as Solver

# This is just an example solver that shows the general form that
# all solvers should take.  They should inherit from the BaseSolver
# class and implement both a correct() and mistakes() method.
# mistakes() may be optional at some point in the future.
class WoodChuckSolver(Solver.BaseSolver):
	def correct(self, params):
		return [(5, 'That is correct!'),]
		
	def mistakes(self, params):
		return [(3, 'Try a little higher.'), (12, 'Nope, lower.')]
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
