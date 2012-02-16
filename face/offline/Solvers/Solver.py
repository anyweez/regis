import face.offline.ParserTools.SolverTools as SolverTools

class BaseSolver(object):
	def __init__(self, qset, template):
		self.qset = qset
		self.template = template 
		
	# Returns a list of values that are correct answers for the provided
	# parameters.  Messages (or None) should be provided as well.
	def correct(self, params):
		raise NotImplementedError
	
	# Returns a list of values that are wrong but should receive customized
	# error messages.
	def mistakes(self, params):
		raise NotImplementedError

	# Called to check the question.  The user's answer is passed in, along
	# with the values that were deemed 'correct' when the self.correct()
	# method was run.  Note that the messages returned from self.correct()
	# are not provided here.  Should return boolean value (true for correct, 
	# false for incorrect).
	def validate(self, answer, valids):
		raise NotImplementedError
	
	def load_userfile(self):
		return SolverTools.load_userfile(self.qset, self.template)
