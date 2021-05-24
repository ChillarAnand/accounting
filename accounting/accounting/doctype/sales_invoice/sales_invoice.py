# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt

from accounting.accounting.doctype.gl_entry.utils import create_gl_entry, create_revere_gl_entry
from frappe.model.document import Document


class SalesInvoice(Document):
	def on_submit(self):
		create_gl_entry(self, self.debit_to, self.total_amount, 0)
		create_gl_entry(self, self.income_account, 0, self.total_amount)

	def on_cancel(self):
		create_revere_gl_entry(self.doctype, self.name)