import imp 

class QuestionSolver(object):
	def __init__(self):
		pass
		
	def solve(self, qid):
		# TODO: Get the solver class for the template from the DB.
		# TODO: Also get the parameter list from the DB.
		solver_name = 'WoodChuckSolver'
		params = { 'days' : 12, 'pounds' : 8 }
		
		f, pn, dsc = imp.find_module(solver_name, ['Solvers'])
		mod = imp.load_module(solver_name, f, pn, dsc)
		
		solver = mod.__dict__[solver_name]()
		answers = {}
		
		# Compute all correct answers.
		answers['correct'] = solver.correct(params)
		
		# Compute all common mistakes.
		answers['mistakes'] = solver.mistakes(params)

		# Return a dictionary like the one below.
		# answers:
		#   correct:
		#     [(5, None),
		#     (10, None)]
		#   mistakes:
		#     [(7, 'Try doing something else instead.'),
		#     (11, 'Nope, a bit too high.')]
		return answers

if __name__ == '__main__':
	qs =QuestionSolver()
	sols = qs.solve(3)
	print sols
