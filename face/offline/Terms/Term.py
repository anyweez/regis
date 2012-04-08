import face.util.FileManager as FileManager

class BaseTerm(object):
    def __init__(self):
        # TODO: Move term_focus code into constructors in Terms.
#        self.user = None
        self.template = None
        self.instance = None
        
    def execute(self, params):
        raise NotImplementedError

    '''
    Some library functions that can be used by other terms.
    '''  

    # get_contents fetches the contents of a file from the
    # appropriate directory.
    def get_full_file(self, filename):
        directory = '../resources/full'

        fp = open('%s/%s' % (directory, filename))
        lines = fp.readlines()
        fp.close()

        return lines

    def store_file(self, content):
        files = FileManager.FileManager()
        files.save_file(self.template, self.instance, content)
        
        return 'question/files/%d' % self.template.id
    # make_sets takes a list of lines (read from a file) and
    # converts them into sets.  This is currently determined
    # by the presence of an empty line between sets.
    def make_sets(self, lines):
        sets = []
        current = []

        for line in lines:
            if len(line) is 0:
                sets.append(current)
                current = []
            else:
                current.append(line.strip())

        return sets
