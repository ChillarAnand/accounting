# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt
import frappe
from accounting.accounting.doctype.gl_entry.utils import create_gl_entry, create_revere_gl_entry
from frappe.model.document import Document
from tests.utils import get_or_create_doc


class SalesInvoice(Document):
	def on_submit(self):
		create_gl_entry(self, self.debit_to, self.total_amount, 0)
		create_gl_entry(self, self.income_account, 0, self.total_amount)
	
	def on_cancel(self):
		self.ignore_linked_doctypes = ('GL Entry',)
		create_revere_gl_entry(self.doctype, self.name)
		
		
@frappe.whitelist(allow_guest=True)
def add_to_cart(username, item_name):
	item = frappe.get_value('Item', {'item_code': item_name}, ['name', 'item_code'])
	user = frappe.get_value('User', {'name': username}, ['name', 'email'], as_dict=1)
	
	_, party = get_or_create_doc({
		'doctype': 'Party',
		'filters': {
			'party_name': user['name'],
		}
	})

	_, party = get_or_create_doc({
		'doctype': 'Sales Invoice',
		'filters': {
			'party': party['name'],
			'docstatus': 0,
		},
	})
