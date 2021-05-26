# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FiscalYear(Document):
	def validate(self):
		if self.end_date < self.start_date:
			frappe.throw('End date should not be less than start date')
