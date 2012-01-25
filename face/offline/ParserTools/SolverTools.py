import os

# ParserTools class
class SolverTools(object):
    def __init__(self):
        self.qset = None
        self.template = None
    
    # Called before running any PT functions in a term definition.
    def term_focus(self, term):
        self.qset = term.qset
        self.template = term.template
    
    # Called after running all PT functions in a term definition.
    def term_unfocus(self):
        self.qset = None
        self.template = None
    
    # Load a full datafile.
    def load_datafile(self, filename):
        directory = '../resources/full'

        fp = open('%s/%s' % (directory, filename))
        lines = fp.readlines()
        fp.close()

        return lines

    # Stores a file for the user that's currently being parsed.
    def store_userfile(self, contents):
        directory = '../resources/user'

        fp = open('%s/%d.%d.txt' % (directory, self.qset.id, self.template.id), 'w')
        for content in contents:
            fp.write('%s\n' % content)
        fp.close()
        
        return 'question/files/%d' % self.template.id

    def prepare_params(self, params):
        finals = {}
        for key in params:
            val = params[key]
            if tuple(val) == val or list(val) == val:
                finals[key] = val[0]
            else:
                finals[key] = val
        
        return finals
                
    def make_sets(self, lines):
        sets = []
        current = []

        for line in lines:
            if len(line.strip()) is 0:
                sets.append(current)
                current = []
            else:
                current.append(line.strip())
        
        # Add the last set, which likely won't end with a newline.
        if len(current) > 0:
            sets.append(current)
        
        return sets