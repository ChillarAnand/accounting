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


def get_or_create_doc(fields=None, dt=None):
    if not dt:
        dt = fields.pop('doctype')
    
    key = fields.get('key')
    dn = None
    
    if key:
        dn = fields[key]
        
    if dn:
        doc = frappe.get_doc(dt, dn)
        created = False

    else:
        try:
            doc = frappe.get_doc(dt, fields)
            created = False
        except frappe.exceptions.DoesNotExistError as e:
            doc = frappe.new_doc(dt)
            if fields:
                for key, value in fields.items():
                    setattr(doc, key, value)
                    
            doc.insert()
            doc.save()
            created = True

    return created, doc
