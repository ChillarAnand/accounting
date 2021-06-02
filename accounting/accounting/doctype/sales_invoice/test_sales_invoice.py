# Copyright (c) 2021, ac and Contributors
# See license.txt

import frappe
import unittest

from tests.utils import get_or_create_doc


class TestSalesInvoice(unittest.TestCase):
	def setUp(self) -> None:
		self.doctype = 'Sales Invoice'
		
	def setup_invoice(self):
		_, self.party = get_or_create_doc(dt='Party', fields={'party_name': 'Frappe'})
		item = {
			'doctype': 'Item',
			'key': 'item_code',
			'item_code': 'board-1',
			'item_name': 'Board',
			'rate': 10,
		}
		_, self.item = get_or_create_doc(fields=item)
		invoice_item = {
			'doctype': 'Sales Invoice Item',
			'item': item['item_name'],
			'quantity': 1,
		}
		created, self.invoice_item = get_or_create_doc(fields=invoice_item)
		self.json = {
			'doctype': self.doctype,
			'naming_series': 'ACC-SINV-TEST-0001',
			'party': self.party.party_name,
		}

	def test_gl_entries_for_sales_invoice(self):
		gl_entry_count = frappe.db.count('GL Entry')
		
		invoice = self.create_sales_invoice('Frappe', 'Laptop', 2)
		invoice.submit()
		
		new_gl_entry_count = frappe.db.count('GL Entry')
		assert new_gl_entry_count == gl_entry_count + 2
	
		last_gl_entry = frappe.get_last_doc('GL Entry')
		assert not last_gl_entry.is_cancelled
		assert last_gl_entry.credit == invoice.total_amount

	def test_reverse_gl_entries_for_sales_invoice(self):
		gl_entry_count = frappe.db.count('GL Entry')
		
		invoice = self.create_sales_invoice('Frappe', 'Laptop', 2)
		invoice.submit()
		invoice.cancel()
		
		new_gl_entry_count = frappe.db.count('GL Entry')
		assert new_gl_entry_count == gl_entry_count + 4
		
		last_gl_entry = frappe.get_last_doc('GL Entry')
		assert last_gl_entry.is_cancelled
		assert last_gl_entry.credit == invoice.total_amount
	
	@staticmethod
	def create_sales_invoice(party, item_name, quantity):
		invoice = frappe.new_doc("Sales Invoice")
		invoice.party = party
		invoice.posting_date = frappe.utils.nowdate()
		invoice.set("items", [
			{
				"item": item_name,
				"quantity": quantity,
				"rate": 11200,
			}
		])
		invoice.insert()
	
		return invoice
