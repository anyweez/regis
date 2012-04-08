
class FileManager(object):
    base_path = '../resources/user'
    
    def get_file_path(self, template, instance):
        return self.base_path + '/%d.%d.txt' % (template.id, instance.id)
    
    def save_file(self, template, instance, data):
        outfile = open(self.get_file_path(template, instance), 'w')
        outfile.write(data)
        outfile.close()
        
    def load_file(self, template, instance):
        infile = open(self.get_file_path(template, instance))
        data = infile.read()
        infile.close()
        
        if len(data.strip().split('\n')) > 1:
            return data.strip().split('\n')
        else:
            return data
        