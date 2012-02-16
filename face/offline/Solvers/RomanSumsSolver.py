import offline.Solvers.Solver as Solver

class RomanSumsSolver(Solver.BaseSolver):
	def _segment2value(self, segment):
		symbols = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
		values = [1000, 500, 100, 50, 10, 5, 1]
		
		max_index = min([symbols.index(letter) for letter in list(segment)])
		total = values[max_index]
		segment_max_i = list(segment).index(symbols[max_index])
		for i, letter in enumerate(segment):
			if i == segment_max_i:
				continue
			elif letter == segment[segment_max_i]:
				total += values[symbols.index(letter)]
			# If this letter comes before the max char, subtract it from the total
			elif i < segment_max_i:
				total -= values[symbols.index(letter)]
			# If it comes after the max char, add it to the total
			else:
				total += values[symbols.index(letter)]
		
		return total
		
	def r2d(self, roman):
		symbols = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
		
		segments = []	
		current_segment = [roman[0],]	
		# Split into segments.
		#   MVII => ['M', 'VII']
		#   LIX => ['L', 'IX']
		#   XII => ['X', 'II']
		
		for letter in roman[1:]:
			if symbols.index(letter) <= symbols.index(current_segment[0]):
				current_segment.append(letter)
			else:
				segments.append(''.join(current_segment))
				current_segment = [letter,]
		if len(current_segment) > 0:
			segments.append(''.join(current_segment))
		
		segvals = [self._segment2value(seg) for seg in segments]

		return sum(segvals)
	
	def correct(self, st, params):
		# no params, just the data file for this problem.
		rnums = self.load_userfile()
		numsum = sum([self.r2d(rn) for rn in rnums])	

		return [(numsum, None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
