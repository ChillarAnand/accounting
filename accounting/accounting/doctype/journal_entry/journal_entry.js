// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt

function calculate_total(frm, name) {
    var entries = frm.doc.accounting_entries;
    var total = 0;
    for (var i in entries) {
        total = total + entries[i][name];
    }
    return total;
};


frappe.ui.form.on('Journal Entry', 'total_debit', function (frm) {
    var difference = frm.doc.total_debit - frm.doc.total_credit;
    frm.set_value('difference', difference);
});


frappe.ui.form.on('Journal Entry', 'total_credit', function (frm) {
    var difference = frm.doc.total_debit - frm.doc.total_credit;
    frm.set_value('difference', difference);
});


frappe.ui.form.on('Journal Entry Item', 'debit', function (frm, cdt, cdn) {
    var total = calculate_total(frm, 'debit');
    frm.set_value('total_debit', total);
});


frappe.ui.form.on('Journal Entry Item', 'credit', function (frm, cdt, cdn) {
    var total = calculate_total(frm, 'credit');
    frm.set_value('total_credit', total);
});


frappe.ui.form.on("Journal Entry", {
    refresh: function (frm, cdt, cdn) {
        frm.set_query("account", "accounting_entries", function (doc) {
            return {
                "filters": {
                    'is_group': 0,
                }
            };
        })
    }
});


frappe.ui.form.on('Journal Entry', {
   refresh: function (frm) {
       frm.add_custom_button(__('General Ledger Report'), function (){
           frappe.route_options = {
               'voucher_no': frm.doc.name,
           };
           frappe.set_route('query-report', 'General Ledger');
       })
   }
});
