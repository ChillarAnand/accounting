// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt


frappe.ui.form.on('Purchase Invoice Item', {
    quantity: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "amount", child.quantity*child.rate);
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


frappe.ui.form.on('Purchase Invoice Item', 'amount', function(frm, cdt, cdn) {
    var items = frm.doc.items;
    var total = 0;
    for(var i in items) {
        total = total + items[i].amount;
    };
    frm.set_value('total_quantity', total);
});
