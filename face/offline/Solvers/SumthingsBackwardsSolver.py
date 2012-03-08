import face.offline.Solvers.Solver as Solver

class SumthingsBackwardsSolver(Solver.BaseSolver):
	def correct(self, st, params):
		p = st.prepare_params(params)

		# Cast the two numbers as strings and reverse the strings.
		first = str(p['num1'])[::-1]
		second = str(p['num2'])[::-1]
		
		# Cast the reversed strings back into numbers and add them.
		return [(int(first) + int(second), None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
