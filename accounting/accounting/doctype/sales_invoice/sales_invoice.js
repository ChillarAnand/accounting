// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt


frappe.ui.form.on("Sales Invoice", "onload", function (frm) {
    frm.set_query("party", function () {
        return {
            "filters": {
                "party_type": "Customer"
            }
        };
    });

    frm.set_query("debit_to", function () {
        return {
            "filters": {
                "root_type": "Accounts Receivable",
                'is_group': 0,
            }
        };
    });

    frm.set_query("income_account", function () {
        return {
            "filters": {
                "root_type": "Income",
                'is_group': 0,
            }
        };
    });

    frm.toggle_display("opening_balance", frm.doc.is_group == 1);
});


frappe.ui.form.on('Sales Invoice', {
    refresh: function (frm) {
        if (frm.doc.docstatus == 1) {

            frm.add_custom_button(__('Create Payment Entry'), function () {
                frappe.route_options = {
                    'party': frm.doc.party,
                    'amount': frm.doc.total_amount,
                    'voucher_type': 'Sales Invoice',
                    'voucher_no': frm.doc.name,
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


frappe.ui.form.on('Sales Invoice', 'is_group', function (frm, cdt, cdn) {
    console.log('aaa');
    frm.toggle_display("opening_balance", frm.doc.is_group == 1);
});

frappe.ui.form.on("refresh", function (frm) {
    console.log('aaa');
    frm.toggle_display("opening_balance", frm.doc.is_group == 1);
});


frappe.ui.form.on('Sales Invoice Item', 'item', function (frm, cdt, cdn) {
    var item = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, 'quantity', 1);
});


frappe.ui.form.on('Sales Invoice Item', 'quantity', function (frm, cdt, cdn) {
    var item = locals[cdt][cdn];
    var amount = item.quantity * item.rate;
    frappe.model.set_value(cdt, cdn, 'amount', amount);
});


frappe.ui.form.on('Sales Invoice Item', 'rate', function (frm, cdt, cdn) {
    var item = locals[cdt][cdn];
    var amount = item.quantity * item.rate;
    frappe.model.set_value(cdt, cdn, 'amount', amount);
});


frappe.ui.form.on('Sales Invoice Item', 'amount', function (frm, cdt, cdn) {
    var items = frm.doc.items;
    var total_amount = 0;
    for (var i in items) {
        total_amount = total_amount + items[i].amount;
    }
    ;
    frm.set_value('total_amount', total_amount);
});


frappe.ui.form.on('Sales Invoice Item', 'quantity', function (frm, cdt, cdn) {
    var items = frm.doc.items;
    var total = 0;
    for (var i in items) {
        total = total + items[i].quantity;
    }
    ;
    frm.set_value('total_quantity', total);
});
