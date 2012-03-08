import face.offline.Solvers.Solver as Solver

class MallCopSolver(Solver.BaseSolver):
	def correct(self, st, params):
		times = self.load_userfile()
		
		arrivals = []
		departures = []
		for time in times:
			arrival, departure = time.split(' ')
			arrivals.append(int(arrival))
			departures.append(int(departure))
			
		# Get the range of times that we need to check
		finish = max(departures)
		occupancy = [0 for x in xrange(finish+1)]
			
		# For each of the time pairs, increment the appropriate
		# occupancy counts.
		for i in xrange(len(arrivals)):
			for oc in xrange(arrivals[i], departures[i]+1):
				occupancy[oc] += 1
		
		return [
			(max(occupancy), None),
			]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
