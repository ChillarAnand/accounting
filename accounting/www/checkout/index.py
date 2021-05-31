import frappe

def get_context(context):
    invoice = frappe.get_all('Sales Invoice', filters={'docstatus': 0}, fields=['*'])[0]
    invoice = frappe.get_doc('Sales Invoice', invoice.name)
    context.invoice = invoice
    return context
