// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt


frappe.ui.form.on('Purchase Invoice', 'onload', function (frm) {
    frm.set_query('party', function () {
        return {
            'filters': {
                'party_type': 'Supplier'
            }
        };
    });

    frm.set_query('credit_to', function () {
        return {
            'filters': {
                'root_type': 'Accounts Payable',
                'is_group': 0,
            }
        };
    });

    frm.set_query('expense_account', function () {
        return {
            'filters': {
                'root_type': 'Expense',
                'is_group': 0,
            }
        };
    });

    frm.add_custom_button(__('Create Payment Entry'), function () {
    });

});


frappe.ui.form.on('Purchase Invoice', {
    refresh: function (frm) {
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Create Payment Entry'), function () {
                frappe.route_options = {
                    'party': frm.doc.party,
                    'amount': frm.doc.total_amount,
                };
                frappe.set_route('Form', 'Payment Entry', 'new-payment-entry');
            });

            frm.add_custom_button(__('General Ledger Report'), function () {
                frappe.route_options = {
                    'voucher_no': frm.doc.name,
                };
                frappe.set_route('query-report', 'General Ledger');
            });
        }
    }
});

frappe.ui.form.on('Purchase Invoice Item', {
    quantity: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "amount", child.quantity * child.rate);
    },
    item: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "quantity", 1);
    }
});


frappe.ui.form.on('Purchase Invoice Item', 'amount', function (frm, cdt, cdn) {
    var items = frm.doc.items;
    var total_amount = 0;
    for (var i in items) {
        total_amount = total_amount + items[i].amount;
    }
    ;
    frm.set_value('total_amount', total_amount);
});


frappe.ui.form.on('Purchase Invoice Item', 'quantity', function (frm, cdt, cdn) {
    var items = frm.doc.items;
    var total = 0;
    for (var i in items) {
        total = total + items[i].quantity;
    }
    ;
    frm.set_value('total_quantity', total);
});
