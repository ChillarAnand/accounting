# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JournalEntry(Document):
	def validate(self):
		if self.difference != 0:
			frappe.throw('Total debit is not equal to total credit.')
