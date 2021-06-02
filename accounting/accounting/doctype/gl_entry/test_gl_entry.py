# Copyright (c) 2021, ac and Contributors
# See license.txt

import frappe
import unittest

from accounting.accounting.doctype.sales_invoice.test_sales_invoice import TestSalesInvoice


class TestGLEntry(unittest.TestCase):
	def setUp(self) -> None:
		self.doctype = 'GL Entry'
	
	def test_gl_entries_for_sales_invoice(self):
		gl_entry_count = frappe.db.count(self.doctype)
		
		invoice = TestSalesInvoice.create_sales_invoice('Frappe', 'Laptop', 2)
		invoice.submit()
		
		new_gl_entry_count = frappe.db.count('GL Entry')
		assert new_gl_entry_count == gl_entry_count + 2
		
		last_gl_entry = frappe.get_last_doc('GL Entry')
		assert not last_gl_entry.is_cancelled
		assert last_gl_entry.credit == invoice.total_amount
	
	def test_reverse_gl_entries_for_sales_invoice(self):
		gl_entry_count = frappe.db.count('GL Entry')
		
		invoice = TestSalesInvoice.create_sales_invoice('Frappe', 'Laptop', 2)
		invoice.submit()
		invoice.cancel()
		
		new_gl_entry_count = frappe.db.count('GL Entry')
		assert new_gl_entry_count == gl_entry_count + 4
		
		last_gl_entry = frappe.get_last_doc('GL Entry')
		assert last_gl_entry.is_cancelled
		assert last_gl_entry.credit == invoice.total_amount
