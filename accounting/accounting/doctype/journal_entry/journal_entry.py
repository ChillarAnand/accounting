# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt

import frappe
from accounting.accounting.doctype.gl_entry.utils import create_gl_entry
from frappe.model.document import Document


class JournalEntry(Document):
	def validate(self):
		if self.difference != 0:
			frappe.throw('Total debit is not equal to total credit.')

	def on_submit(self):
		for account in self.accounting_entries:
			if account.debit:
				create_gl_entry(self, account.account, account.debit, 0, party=account.party)
			if account.credit:
				create_gl_entry(self, account.account, 0, account.credit, party=account.party)
