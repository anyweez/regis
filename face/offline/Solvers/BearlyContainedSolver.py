import face.offline.Solvers.Solver as Solver

class BearlyContainedSolver(Solver.BaseSolver):
	def correct(self, st, params):
		nums = self.load_userfile()
		
		xcoords = []
		ycoords = []
		
		for num in nums:
			x, y = num.split()
			xcoords.append(int(x))
			ycoords.append(int(y))
		
		horiz = 2 * (max(xcoords) - min(xcoords))
		vert = 2 * (max(ycoords) - min(ycoords))
		
		return [(horiz + vert, None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
