import face.offline.Solvers.Solver as Solver

class ScrambledStatementsSolver(Solver.BaseSolver):
	def op_reverse(self, phrase):
		phrase.reverse()
		
		return phrase
	
	def op_frontback(self, phrase):
		phrase.append(phrase.pop(0))
		
		return phrase
	
	def op_duplicate(self, phrase):
		phrase.insert(2, phrase[1])
	
		return phrase
	
	def correct(self, st, params):
		p = st.prepare_params(params)
		phrase = list(str(p['phrase'][0]))
		operations = self.load_userfile()

		for op in operations:
			if op == 'reverse':
				phrase = self.op_reverse(phrase)
			elif op == 'frontback':
				phrase = self.op_frontback(phrase)
			elif op == 'duplicate':
				phrase = self.op_duplicate(phrase)
			else:
#				print op
				raise Exception('Unknown input operation...no idea what to do!')

		return [(''.join(phrase), None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
