import frappe

def get_context(context):
    items = frappe.get_all('Item', filters={'show_in_website': True}, fields=['*'])
    context.items = items
    return context
