import face.offline.Solvers.Solver as Solver

class GoingUpSolver(Solver.BaseSolver):
	def correct(self, st, params):
		numbers = [int(num) for num in self.load_userfile()]

		lastnum = -1
		counter = 0
		max_counter = 0
		for num in numbers:
			# If the current number is larger than the last one,
			# increment the counter.
			if num > lastnum:
				counter += 1
			# If not, check to see if we need to store the current
			# counter value and do it if needed.  Reset the counter.
			else:
				if counter > max_counter:
					max_counter = counter
				counter = 0
			lastnum = num
			
		# Check the ending value of the counter.
		if counter > max_counter:
			max_counter = counter
			
		return [(max_counter, None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]