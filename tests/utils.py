import frappe


def get_or_create_doc(params):
    dn = params[params['key']]
    doc = frappe.db.exists(params['doctype'], dn)
    if doc:
        return frappe.get_doc(params['doctype'], dn)
    else:
        return frappe.get_doc(params).insert()
