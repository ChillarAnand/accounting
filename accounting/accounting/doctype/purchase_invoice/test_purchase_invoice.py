# Copyright (c) 2021, ac and Contributors
# See license.txt
import unittest

import frappe
from frappe import ValidationError


class TestPurchaseInvoice(unittest.TestCase):
	def test_purchase_invoice_validation_errors(self):
		with self.assertRaises(ValidationError):
			self.create_purchase_invoice('Frappe', 'Laptop', 0)
			self.create_purchase_invoice('Frappe', 'Laptop', -1)
	
	def test_create_purchase_invoice(self):
		invoice = self.create_purchase_invoice('Frappe', 'Laptop', 2)
		invoice.submit()
		
		total = sum(item.quantity * item.rate for item in invoice.items)
		assert invoice.total_amount == total
	
	@staticmethod
	def create_purchase_invoice(party, item_name, quantity):
		invoice = frappe.new_doc("Purchase Invoice")
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
