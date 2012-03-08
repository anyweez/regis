import face.offline.Solvers.Solver as Solver

class AgeOfInnocenceSolver(Solver.BaseSolver):
	def correct(self, st, params):
		dates = self.load_userfile()

		decades = [0 for x in xrange(10)]
		for date in sorted(dates):
			decades[int(date[2])] += 1

		# Get the winning decade.  WINNER = 7 if the 70's
		# were the most common.
		winner = decades.index(max(decades))
		return [(1900 + (winner * 10), None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]