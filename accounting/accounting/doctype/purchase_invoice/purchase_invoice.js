// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt


frappe.ui.form.on('Purchase Invoice', 'onload', function(frm){
    frm.set_query('party', function() {
        return {
            'filters': {
                'party_type': 'Supplier'
            }
        };
    });

    frm.set_query('credit_to', function() {
        return {
            'filters': {
                'parent_account': 'Accounts Payable'
            }
        };
    });

    frm.set_query('expense_account', function() {
        return {
            'filters': {
                'parent_account': 'Expense'
            }
        };
    });

});


frappe.ui.form.on('Purchase Invoice Item', {
    quantity: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "amount", child.quantity * child.rate);
    },
    item: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "quantity", 1);
    }
});


frappe.ui.form.on('Purchase Invoice Item', 'amount', function(frm, cdt, cdn) {
    var items = frm.doc.items;
    var total_amount = 0;
    for(var i in items) {
        total_amount = total_amount + items[i].amount;
    };
    frm.set_value('total_amount', total_amount);
});


frappe.ui.form.on('Purchase Invoice Item', 'quantity', function(frm, cdt, cdn) {
    var items = frm.doc.items;
    var total = 0;
    for(var i in items) {
        total = total + items[i].quantity;
    };
    frm.set_value('total_quantity', total);
});
