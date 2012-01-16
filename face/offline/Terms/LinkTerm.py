import offline.Terms.Term as Term
import offline.ParserTools.ParserTools as ParserTools

import random

# 'mixset' is a term that can be used to randomly select
# a set from a file and scramble all of the elements in
# the set.  It has two arguments, one required and one
# optional.
#    mixset setfile.txt [setlength]

class LinkTerm(Term.BaseTerm):
    def execute(self, params):
        contents = params[0]
        
        pt = ParserTools.ParserTools()
        
        pt.term_focus(self)
        url = pt.store_userfile(contents[0])
        pt.term_unfocus()
        
        link = '[[%s]]' % url
        return (link, link)
