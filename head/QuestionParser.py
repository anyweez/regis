import imp, os, re

'''
Parses a question and returns the new question string as well as the
parameters that were used to complete the string.
'''
class QuestionParser(object):
	def __init__(self):
		pass
		
	def parse(self, qtxt):
		# Replace each [*] with the appropriate value.
		lines = [x.strip() for x in qtxt.split('\n') if len(x.strip()) > 0]
		
		variables = {}
		question = []
		# Get a value for each variable
		for line in lines:
			# If this line contains a variable def, handle it
			if line[0] == ';':
				var_name, var_def = [x.strip() for x in line[1:].split(':')]
				def_components = var_def.split(' ')

				# Figure out what the handler module's name is.  There's a simple
				# formula for doing this based on the name of the defining function.
				mod_name = '%sTerm' % def_components[0].capitalize()
				
				f, pn, dsc = imp.find_module(mod_name, ['Terms'])
				mod = imp.load_module(mod_name, f, pn, dsc)
				
				term_obj = mod.__dict__[mod_name]()
				# Each variable entry has two values: the human-readable
				# and the machine-readable version.  If the execute method
				# returns a list or tuple, populate the two fields with
				# different values.  If it returns a single value, put
				# that in both slots. 
				#
				# Format:
				#   variables[var_name] = (display_value, store_value)
				returned = term_obj.execute(def_components[1:])
				try:
					variables[var_name] = tuple(returned[0:2])
				except TypeError:
					variables[var_name] = (returned, returned)
		
			else:
				question.append(line)

		# Replace the variables with the appropriate values.
		for i, line in enumerate(question):
			strvars = list(set(re.findall('(?<=\[)[a-zA-Z1-9]*(?=\])', line)))
			for var in strvars:
				line = re.sub('\[%s\]' % var, str(variables[var][0]), line, count=10)
			question[i] = line

		return ('\n'.join(question), variables)
			

if __name__ == '__main__':
	qp = QuestionParser()
	
	question = 'A wood chuck chucks [pounds] pounds of wood in [days] days.\n\n; pounds: num 1 20\n; days: num 3 5'
	newq, params = qp.parse(question)
	
	print 'Input: %s' % question
	print 'Output: %s' % newq
	print 'Params: %s' % str(params)
