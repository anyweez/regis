import face.offline.Solvers.Solver as Solver

class OnceIsEnoughSolver(Solver.BaseSolver):
	def correct(self, st, params):
		text = self.load_userfile()
		
		letter_flags = {}
		keepers = []

		# Iterate through each character, keeping it only if its
		# the first time it has appeared (tracked using LETTER_FLAGS).
		for char in text[0].strip():
			if not letter_flags.has_key(char):
				letter_flags[char] = True
				keepers.append(char)

		# Casing doesn't matter that much, so a lowercased version should
		# be accepted as well.		
		return [
			((''.join(keepers), ''.join(keepers)), None),
			((''.join(keepers).lower(), ''.join(keepers).lower()), None)
			]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
