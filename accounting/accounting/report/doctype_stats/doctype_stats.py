# Copyright (c) 2013, ac and contributors
# For license information, please see license.txt

# import frappe

def execute(filters=None):
	print(filters)
	print('eeeeee')
	columns, data = [], []
	return columns, data


columns = [
	{
		'fieldname': 'name',
		'label': 'Table',
		'fieldtype': 'Data',
		'options': 'Account',
		'width': '200px',
	},
	{
		'fieldname': 'count',
		'label': 'Count',
		'fieldtype': 'Data',
		'options': 'Currency',
		'width': '100px',
		
	}
]


def db_stats(column=None, duration=1, include_emtpy=False):
	sql = '''
	SELECT table_name FROM information_schema.tables
	where table_type = 'BASE TABLE'
	;
	'''
	
	tables = frappe.db.sql(sql)
	
	stats = {}
	
	for table in tables:
		query = f'''
		select
			count(*)
		FROM
			`{table[0]}`
		'''
		
		try:
			data = frappe.db.sql(query)
		except Exception as e:
			continue
		
		stats[table[0].lstrip('tab')] = data[0][0]
	
	return stats


column = filters.get('column')

stats = db_stats(column=column)
sorted_stats = stats
sorted_stats = {k: v for k, v in sorted(stats.items(), key=lambda item: -item[1])}

data = []
for key, value in sorted_stats.items():
	data.append({
		'name': key,
		'count': value,
	})

data = columns, data
