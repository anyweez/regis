import offline.Solvers.Solver as Solver
import offline.ParserTools.SolverTools as SolverTools

class PrimeFinderSolver(Solver.BaseSolver):
	def correct(self, params):
		st = SolverTools.SolverTools()
		maxcap = int(st.prepare_params(params)['ht']) * 10000

		primes = self.sieve(maxcap)
		avg = int(round(sum(primes) / len(primes)))

		return [(avg, None),]
	
	def sieve(self, maxnum):
		numlist = [i+2 for i in xrange(maxnum-2)]
		primes = []
		
		while len(numlist) > 0:
			primes.append(numlist.pop(0))
			
			# Remove all numbers that have the new num as a factor
			numlist = [num for num in numlist if num % primes[-1] != 0]
			
		return primes
		
	def next_largest(self, lower, numlist):
		for num in numlist:
			if num > lower:
				return num
		return None
	
	
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
