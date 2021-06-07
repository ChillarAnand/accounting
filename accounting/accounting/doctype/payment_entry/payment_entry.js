// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt


frappe.ui.form.on('Payment Entry', 'onload', function (frm) {
    frm.set_query('party', function () {
        return {
            'filters': {
                'party_type': frm.doc.party_type
            }
        }
    })

    frm.set_query('party', function () {
        return {
            'filters': {
                'party_type': frm.doc.party_type
            }
        }
    })

    frm.set_query("account_paid_from", function () {
        if (frm.doc.payment_type == 'Pay') {
            return {
                'filters': {
                    'is_group': 0,
                    'root_type': 'Asset',
                }
            };
        } else {
            return {
                'filters': {
                    'is_group': 0,
                }
            };
        }
    });

    frm.set_query("account_paid_to", function () {
        if (frm.doc.payment_type == 'Pay') {
            return {
                'filters': {
                    'is_group': 0,
                }
            };
        } else {
            return {
                'filters': {
                    'is_group': 0,
                    'root_type': 'Asset',

                }
            };
        }
    });

})
