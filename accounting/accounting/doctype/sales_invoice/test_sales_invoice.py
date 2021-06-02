# Copyright (c) 2021, ac and Contributors
# See license.txt
import unittest

import frappe
from frappe import ValidationError


class TestSalesInvoice(unittest.TestCase):
	def test_sales_invoice_validation_errors(self):
		with self.assertRaises(ValidationError):
			self.create_sales_invoice('Frappe', 'Laptop', -1)
		
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
