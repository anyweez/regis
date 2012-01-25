import offline.Solvers.Solver as Solver
import offline.ParserTools.SolverTools as SolverTools

class TimeForAChangeSolver(Solver.BaseSolver):
	def correct(self, params):
		st = SolverTools.SolverTools()
		params = st.prepare_params(params)

		cents = 8#int(params['cents']) * (int(params['dollars']) * 100)

		coins = [25, 10, 5, 1]

		return [(self.count_possibilities(cents, coins), None),]
	
	def count_possibilities(self, total, coins):
		if len(coins) is 0:
			return 0
		if total < min(coins) or total < 0:
			return 0
		if total is 0:
			return 1
		
		return self.count_possibilities(total - coins[0], coins) + self.count_possibilities(total, coins[1:])
	
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
