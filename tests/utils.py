import frappe


# def get_or_create_doc(params):
#     print(params)
#
#     dn = params[params['key']]
#     doc = frappe.db.exists(params['doctype'], dn)
#     if doc:
#         created = False
#     else:
#         created = True
#         doc = frappe.get_doc(params).insert()
#
#     return created, doc


def get_or_create_doc(params):
    doc = frappe.get_all(params['doctype'], filters=params['filters'])
    if doc:
        created = False
        doc = doc[0]
    else:
        created = True
        doc = frappe.get_doc({
            'doctype': params['doctype'],
            **params['filters'],
        }).insert()

    return created, doc
