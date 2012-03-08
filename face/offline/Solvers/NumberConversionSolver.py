import face.offline.Solvers.Solver as Solver

class NumberConversionSolver(Solver.BaseSolver):
	def correct(self, st, params):
		number = int(st.prepare_params(params)['number'])
		bin_digits = []
		
		greatest_pwr = 1
		while (2 ** greatest_pwr) < number:
			greatest_pwr += 1
			
		greatest_pwr -= 1
		
		while greatest_pwr >= 0:
			if number >= (2 ** greatest_pwr):
				bin_digits.append(1)
				number -= (2 ** greatest_pwr)
			else:
				bin_digits.append(0)
				
			greatest_pwr -= 1
		
		return [(''.join([str(n) for n in bin_digits]), None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
