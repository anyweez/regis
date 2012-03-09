import face.offline.Solvers.Solver as Solver
import math

class EvenSplitSolver(Solver.BaseSolver):
	def correct(self, st, params):
		# no params, just the data file for this problem.
		text = self.load_userfile()[0]
		words = [word.strip('.,;"\'') for word in text.strip().split(' ') if len(word) > 0]

		middle = len(words) / 2
		if len(words) % 2 == 0:
			return [
				('%s %s' % ( words[middle-1], words[middle] ), None),
			]
		else:
			return [
				('%s' %  words[int(math.ceil(round(middle)))], None),
			]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
