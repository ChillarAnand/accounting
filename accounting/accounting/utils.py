def get_fiscal_date_range(now):
	year = now.year
	month = now.month
	
	if month > 3:
		from_date = '{}-04-01'.format(year)
		to_date = '{}-03-31'.format(year + 1)
	else:
		from_date = '{}-04-01'.format(year - 1)
		to_date = '{}-03-31'.format(year)
	return from_date, to_date
