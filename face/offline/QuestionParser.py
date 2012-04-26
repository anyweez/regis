import imp, re, json
import face.models.models as models

'''
Parses a question and returns the new question string as well as the
parameters that were used to complete the string.
'''
class QuestionParser(object):
	permutations = {
		'auto' : 100,
		'peer' : 1
	}
	
	def __init__(self):
		self.user = None
		
	def process(self, template):
		num_instances = models.QuestionInstance.objects.filter(template=template, active=True).count()
		try:
			req_instances = self.permutations[template.type]
		except KeyError:
			raise Exception('Invalid template type for #%d: %s' % (template.id, template.type))
		
		print 'Parsing %d / %d instances of template #%d' % (req_instances - num_instances, req_instances, template.id)
			
		for i in xrange(req_instances - num_instances):
			instance = models.QuestionInstance(template=template, text='', variables='')
			instance.save()

			try:			   
				text, values = self.parse(template, instance)
				
				instance.text = text
				instance.variables = json.dumps(values)
				instance.save()
				# If there are any errors, let's delete them.
			except Exception as e:
				instance.delete()
				print e
					
		template.status = 'pending'
		template.save()
			
	def parse(self, template, instance):
		# Replace each [*] with the appropriate value.
		lines = [x.strip() for x in template.text.split('\n') if len(x.strip()) > 0]
		
		variables = {}
		question = []
		# Get a value for each variable
		for line in lines:
			# If this line contains a variable def, handle it
			if line[0] == ';':
				var_name, var_def = [x.strip() for x in line[1:].split(':')]
				def_components = var_def.split(' ')

				# Replace the value with the variable's name.  The variable that's
				# used as part of a definition must be defined first.
				for i, var in enumerate(def_components[1:]):
					if variables.has_key(var):
						def_components[i+1] = variables[var]

				# Figure out what the handler module's name is.  There's a simple
				# formula for doing this based on the name of the defining function.
				mod_name = '%sTerm' % def_components[0].capitalize()
				
				f, pn, dsc = imp.find_module(mod_name, ['offline/Terms'])
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
				term_obj.template = template
				term_obj.instance = instance
				
				returned = term_obj.execute(def_components[1:])
				try:
					variables[var_name] = tuple(returned[0:2])
				except TypeError:
					variables[var_name] = (returned, returned)
		
			else:
				question.append(line)

		# Replace the variables with the appropriate values.
		for i, line in enumerate(question):
			strvars = list(set(re.findall('(?<=\[)[a-zA-Z1-9_]*(?=\])', line)))
			for var in strvars:
				line = re.sub('\[%s\]' % var, str(variables[var][0]), line, count=10)
			question[i] = line

		return ('\n'.join(question), variables)
