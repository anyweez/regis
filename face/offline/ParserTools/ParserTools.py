import os

# ParserTools class
class ParserTools(object):
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
        finals = []
        for param in params:
            if tuple(param) == param or list(param) == param:
                finals.append(param[0])
            else:
                finals.append(param)
                
        if len(finals) is 1:
            return finals[0]
        else:
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