import face.offline.Solvers.Solver as Solver

class FreakyFridaysSolver(Solver.BaseSolver):
	def is_friday(self, daydelta):
		return daydelta % 7 == 0

	def is_thirteenth(self, daydelta):
		current_year = 2011
		current_month = 1
		
		while daydelta > self.days_in_month(current_month, current_year):
			daydelta -= self.days_in_month(current_month, current_year)
			current_month += 1
			
			if current_month == 13:
				current_year += 1
				current_month = 1

		return daydelta == 13

	def days_in_month(self, month, year):
		days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		if self.is_leap_year(year):
			days[1] = 29
		else:
			days[1] = 28
		return days[month-1]
		
	def is_leap_year(self, year):
		return year % 4 == 0
	
	def correct(self, st, params):
		p = st.prepare_params(params)
		
		year = int(p['year'])
		day = int(p['day'])
		month = int(p['month'])
		num_targets = 0
		
		days_until = (day - 1)
		# Add all of the days for each year.
		if year > 2011:
			for y in xrange(2011, year):
				if self.is_leap_year(y):
					days_until += 366
				else:
					days_until += 365
				
		# Add all of the days for each month.
		if month > 1:
			for m in xrange(1, month):
				days_until += self.days_in_month(m,	year)

		for day in xrange(1, days_until+1):
			if self.is_friday(day) and self.is_thirteenth(day):
				num_targets += 1
		
		return [(num_targets, None),]
		
	def mistakes(self, params):
		return []
		
	def validate(self, answer, valids):
		return str(answer) in [str(v) for v in valids]
