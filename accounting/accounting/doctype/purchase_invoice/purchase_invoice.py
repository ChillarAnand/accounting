# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from accounting.accounting.doctype.gl_entry.utils import create_gl_entry


class PurchaseInvoice(Document):
	def validate(self):
		self.validate_dates()
		
	def validate_dates(self):
		if self.payment_due_date and self.payment_due_date < self.posting_date:
			frappe.throw('Payment due date cannot be before posting date.')
	
	def on_submit(self):
		create_gl_entry(self, self.expense_account, self.total_amount, 0)
		create_gl_entry(self, self.credit_to, 0, self.total_amount)
