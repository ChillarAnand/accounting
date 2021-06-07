import frappe


def get_context(context):
	party = frappe.session.user
	orders = frappe.get_all('Sales Invoice', filters={'party': party}, fields=['*'])
	context.orders = orders
	return context
