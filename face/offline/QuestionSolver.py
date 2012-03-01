import imp, json, sys
import face.models.models as regis

import ParserTools.SolverTools as SolverTools

class QuestionSolver(object):
	def __init__(self):
		pass
		
	def solve(self, question):
		# If the question is provided by the community, it doesn't
		# have a solver and nothing happens here.
		if question.community:
			return None
		
		# Get the name of the solver from the database.
		solver_name = '%sSolver' % (question.template.solver_name)
		# The values of the variables are also stored in the DB.
		params = json.loads(question.variables)
		
		try:
			qset = question.questionset.all()[0]
		except regis.QuestionSet.DoesNotExist:
			print "The question set for this question does not exist.  Fix that before continuing."
			sys.exit(1)
		except IndexError:
			print "The question set for this question has been deleted.  Please run manage.py qpurge."
			print "Note: this will delete this question from the database."
			sys.exit(1)
		
		f, pn, dsc = imp.find_module(solver_name, ['offline/Solvers'])
		mod = imp.load_module(solver_name, f, pn, dsc)
		
		solver = mod.__dict__[solver_name](qset, question.template)
		answers = {}
		
		# Compute all correct answers.
		answers['correct'] = solver.correct(SolverTools, params)
		
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
