import face.offline.Terms.Term as Term

class LinkTerm(Term.BaseTerm):
    def execute(self, params):
        raw_content = params[0][0]

        # If contents is a list, make it into a string.
        if list(raw_content) == raw_content:
            content = '\n'.join(raw_content)
        # Otherwise it's a string so nothing needs to
        # change.
        else:
            content = raw_content
            
        url = self.store_file(content)
        
        link = '[[%s]]' % url
        return (link, link)
