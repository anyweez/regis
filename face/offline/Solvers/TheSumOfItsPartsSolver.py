import face.offline.Solvers.Solver as Solver

class TheSumOfItsPartsSolver(Solver.BaseSolver):
	def decompose_num(self, num):
#		start = int(num) - 1
		start = 1
		values = []

		# start at the midpoint and work your way down
		# search for combinations moving upwards
		# this can probably be optimized by simply keeping
		# track of sums but I'm not going to worry about 
		# that yet.
		while start < num:
			values = [start,]
			while sum(values) < num:
				values.append(values[-1] + 1)
			
			if sum(values) == num:
				return values

			# Decrease the start value and try again.
			start += 1
			
		return None				
	
	def correct(self, st, params):
		p = st.prepare_params(params)
		decomposed = self.decompose_num(p['number'])
		
		if decomposed is not None:
			return [(decomposed[0], None),]
		else:
			return [(0, None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
