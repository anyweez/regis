import face.offline.Solvers.Solver as Solver

class FlippedPhrasesSolver(Solver.BaseSolver):
	def correct(self, st, params):

		text = self.load_userfile()[0]
		
		words = [word.strip('\n .;,') for word in text.split() if len(word) > 0]
		letters = []
		for word in words:
			letters.append(word[-1])
		
		letters.reverse()
		return [(''.join(letters), None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
