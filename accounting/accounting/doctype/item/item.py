# Copyright (c) 2021, ac and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Item(Document):
	pass
	
	# def before_submit(self):
	# 	self.unique_validation()

	# def unique_validation(self):
	# 	item = frappe.get_doc({
	# 		"doctype": "Item",
	# 		"code": self.code,
	# 	})
	# 	if item:
	# 		frappe.throw("Item with code {} already exists".format(self.code))



