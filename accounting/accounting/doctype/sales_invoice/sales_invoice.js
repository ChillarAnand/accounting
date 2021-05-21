// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt


frappe.ui.form.on("Sales Invoice", "onload", function(frm) {
    frm.set_query("party", function() {
        return {
            "filters": {
                "party_type": "Customer"
            }
        };
    });

    frm.set_query("debit_to", function() {
        return {
            "filters": {
                "parent_account": "Accounts Receivable"
            }
        };
    });

    frm.set_query("income_account", function() {
        return {
            "filters": {
                "parent_account": "Income"
            }
        };
    });

});


//frappe.ui.form.on("Sales Invoice Item", {
//	rate: function(frm, cdt, cdn) {
//		frm.set_query("party", function() {
//			return {
//				filters: [
//					["Party", "party_type", "=", "Customer"]
//				]
//			}
//		});
//	}
//});


frappe.ui.form.on('Sales Invoice Item', 'item', function(frm, cdt, cdn) {
    var item = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, 'quantity', 1);
});


frappe.ui.form.on('Sales Invoice Item', 'quantity', function(frm, cdt, cdn) {
    var item = locals[cdt][cdn];
    var amount = item.quantity * item.rate;
     frappe.model.set_value(cdt, cdn, 'amount', amount);
});


frappe.ui.form.on('Sales Invoice Item', 'rate', function(frm, cdt, cdn) {
    var item = locals[cdt][cdn];
    var amount = item.quantity * item.rate;
    frappe.model.set_value(cdt, cdn, 'amount', amount);
});


frappe.ui.form.on('Sales Invoice Item', 'amount', function(frm, cdt, cdn) {
    var items = frm.doc.items;
    var total_amount = 0;
    for(var i in items) {
        total_amount = total_amount + items[i].amount;
    };
    frm.set_value('total_amount', total_amount);
});


frappe.ui.form.on('Sales Invoice Item', 'quantity', function(frm, cdt, cdn) {
    var items = frm.doc.items;
    var total = 0;
    for(var i in items) {
        total = total + items[i].quantity;
    };
    frm.set_value('total_quantity', total);
});


frappe.form.link_formatters['Party'] = function(value, doc) {
    return doc.party_name + ' (' + doc.party_type + ')';
};
