import offline.Terms.Term as Term
import offline.ParserTools.ParserTools as ParserTools
import random

class CaesarTerm(Term.BaseTerm):
	def execute(self, params):
		pt = ParserTools.ParserTools()
		phrase, shift_amt = pt.prepare_params(params)
		
		phrase = phrase[0].lower() # all alpha characters fall in the range [97, 122]
		
		new_ascii = []
		for letter in phrase:
			if letter.isalpha():
				new_ascii.append( (ord(letter) - 97 + shift_amt) % 26 )
			else:
				# Subtract 97 because we're going to be adding it on again in a second.
				new_ascii.append(ord(letter) - 97)
		
		new_chars = [chr(val + 97) for val in new_ascii]
		return (''.join(new_chars), ''.join(new_chars))
