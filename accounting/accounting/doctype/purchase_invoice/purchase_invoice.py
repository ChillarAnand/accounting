# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt

# import frappe
from accounting.accounting.doctype.gl_entry.utils import create_gl_entry
from frappe.model.document import Document


class PurchaseInvoice(Document):
	def on_submit(self):
		print('---------------')
		print(self)
		create_gl_entry(self, self.credit_to, self.total_amount, 0)
		create_gl_entry(self, self.expense_account, 0, self.total_amount)
