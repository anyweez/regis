import face.offline.Solvers.Solver as Solver

class TimeForAChangeSolver(Solver.BaseSolver):
	def correct(self, st, params):
		params = st.prepare_params(params)
		cents = int(params['dollars']) * 100 + int(params['cents']) 

		coins = [25, 10, 5, 1]

		return [(self.count_possibilities(cents, coins), None),]
	
	def count_possibilities(self, total, coins):
		if len(coins) is 0 or total < 0:
			return 0
		elif total is 0:
			return 1
		else:
			return self.count_possibilities(total - coins[0], coins) + self.count_possibilities(total, coins[1:])
	
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
