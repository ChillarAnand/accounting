import frappe


def get_context(context):
	try:
		invoice = frappe.get_all('Sales Invoice', filters={'docstatus': 0}, fields=['*'])[0]
		invoice = frappe.get_doc('Sales Invoice', invoice.name)
	except:
		invoice = frappe.new_doc('Sales Invoice')

	context.invoice = invoice
	return context
