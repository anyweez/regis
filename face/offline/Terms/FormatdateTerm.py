import face.offline.Terms.Term as Term
import face.offline.ParserTools.ParserTools as ParserTools
import datetime

class FormatdateTerm(Term.BaseTerm):
	def execute(self, params):
		pt = ParserTools.ParserTools()
		month, day, year = pt.prepare_params(params)

		datestr = datetime.date(int(year), int(month), int(day)).strftime('%B %d, %Y')
		return (datestr, datestr)
