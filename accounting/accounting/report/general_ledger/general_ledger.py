# Copyright (c) 2013, ac and contributors
# For license information, please see license.txt
import datetime

import frappe
from accounting.accounting.utils import get_fiscal_date_range
from frappe.utils import now


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	columns = [
		{
			"label": "GL Entry",
			"fieldname": "gl_entry",
			"fieldtype": "Link",
			"options": "GL Entry",
			"hidden": 1
		},
		{
			"label": "Posting Date",
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 110
		},
		{
			"label": "Account",
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 180
		},
		{
			"label": "Debit (INR)",
			"fieldname": "debit",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": "Credit (INR)",
			"fieldname": "credit",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": "Balance (INR)",
			"fieldname": "balance",
			"fieldtype": "Float",
			"width": 130
		},
		{
			"label": "Voucher Type",
			"fieldname": "voucher_type",
			"width": 120
		},
		{
			"label": "Voucher No",
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 180
		},
		{
			"label": "Party",
			"fieldname": "party",
			"width": 100
		}
	]
	return columns


def add_balance_column(data):
	for row in data:
		row.balance = (row.debit or 0) - (row.credit or 0)
	return data


def get_db_filters(filters):
	db_filters = {}
	now = datetime.datetime.now()
	from_date = filters.get('from_date')
	if not from_date:
		from_date, _ = get_fiscal_date_range(now)
	
	to_date = filters.get('to_date')
	if not to_date:
		_, to_date = get_fiscal_date_range(now)
	
	db_filters["posting_date"] = ["between", [from_date, to_date]]

	return db_filters


def get_data(filters):
	filters = get_db_filters(filters)
	data = frappe.get_all('GL Entry', fields=['*'], filters=filters)
	data = add_balance_column(data)

	return data
