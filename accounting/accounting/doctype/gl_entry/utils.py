import frappe


def create_gl_entry(doc_type, account, dr, cr, party=None):
    if not party:
        party = doc_type.party

    options = {
        'doctype': 'GL Entry',
        'voucher_type': doc_type.doctype,
        'voucher_no': doc_type.name,
        'posting_date': doc_type.posting_date,
        'account': account,
        'debit_amount': dr,
        'credit_amount': cr,
        'party': party,
    }
    print(options)
    gl_entry = frappe.get_doc(options)
    print(gl_entry)
    gl_entry.insert()
