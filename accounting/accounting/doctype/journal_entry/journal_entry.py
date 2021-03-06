# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt

import frappe
from accounting.accounting.doctype.gl_entry.utils import create_gl_entry
from frappe.model.document import Document
from frappe.utils import flt


class JournalEntry(Document):
	def validate(self):
		self.post_fill()
		self.same_account_validation()
		if self.difference and self.difference != 0:
			frappe.throw('Total debit is not equal to total credit.')

	def on_submit(self):
		for account in self.accounting_entries:
			create_gl_entry(self, account.account, account.debit, account.credit, party=account.party)

	def post_fill(self):
		self.total_debit, self.total_credit, self.difference = 0, 0, 0
		for entry in self.accounting_entries:
			self.total_debit = flt(self.total_debit) + flt(entry.debit)
			self.total_credit = flt(self.total_credit) + flt(entry.credit)

		self.difference = flt(self.total_debit) - flt(self.total_credit)

	def same_account_validation(self):
		debit_accounts = [entry.account for entry in self.accounting_entries if entry.debit]
		credit_accounts = [entry.account for entry in self.accounting_entries if entry.credit]
		intersection = set(debit_accounts).intersection(set(credit_accounts))
		if intersection:
			frappe.throw('You can debit & credit in the same account at a time')
