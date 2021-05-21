# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt

from accounting.accounting.doctype.gl_entry.utils import create_gl_entry
from frappe.model.document import Document


class PaymentEntry(Document):
	def on_submit(self):
		create_gl_entry(self, self.account_paid_to, self.amount, 0)
		create_gl_entry(self, self.account_paid_from, 0, self.amount)
