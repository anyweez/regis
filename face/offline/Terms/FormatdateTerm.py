import offline.Terms.Term as Term
import offline.ParserTools.ParserTools as ParserTools
import random, datetime

class FormatdateTerm(Term.BaseTerm):
	def execute(self, params):
		pt = ParserTools.ParserTools()
		month, day, year = pt.prepare_params(params)

		datestr = datetime.date(int(year), int(month), int(day)).strftime('%B %d, %Y')
		return (datestr, datestr)
