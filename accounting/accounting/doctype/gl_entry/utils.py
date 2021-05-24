import frappe
from frappe.utils import now


def create_gl_entry(doc_type, account, dr, cr, party=None):
    if not party:
        party = doc_type.party

    options = {
        'doctype': 'GL Entry',
        'voucher_type': doc_type.doctype,
        'voucher_no': doc_type.name,
        'posting_date': doc_type.posting_date,
        'account': account,
        'debit': dr,
        'credit': cr,
        'party': party,
    }
    gl_entry = frappe.get_doc(options)
    gl_entry.insert()


def create_revere_gl_entry(voucher_type, voucher_no):
    filters = {
        'voucher_type': voucher_type,
        'voucher_no': voucher_no,
    }
    print(filters)
    gl_entries = frappe.get_all('GL Entry', filters=filters, fields=['*'])

    frappe.db.sql("""UPDATE `tabGL Entry` SET is_cancelled = 1,
        modified=%s, modified_by=%s
        where voucher_type=%s and voucher_no=%s and is_cancelled = 0""",
                  (now(), frappe.session.user, gl_entries[0].voucher_type, gl_entries[0].voucher_no))

    for gl_entry in gl_entries:
        debit_amount = gl_entry.debit_amount
        credit_amount = gl_entry.credit_amount

        gl_entry.name = None
        gl_entry.debit_amount = credit_amount
        gl_entry.credit_amount = debit_amount
        gl_entry.remarks = 'Cancelled'
        gl_entry.is_cancelled = 1

        new_gl_entry = frappe.new_doc('GL Entry')
        new_gl_entry.update(gl_entry)
        new_gl_entry.insert()
        new_gl_entry.submit()
