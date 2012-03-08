import face.offline.Solvers.Solver as Solver

class LargerMirrorSolver(Solver.BaseSolver):
	def is_palindrome(self, num):
		if len(num) <= 1:
			return True
		elif num[0] == num[-1]:
			return self.is_palindrome(num[1:-1])
		else:
			return False
	
	def correct(self, st, params):
		p = st.prepare_params(params)

		num = int(p['min_pal'])
		while not self.is_palindrome(str(num)):
			num += 1

		return [(num, None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
