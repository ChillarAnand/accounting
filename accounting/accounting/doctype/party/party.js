// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt

frappe.ui.form.on('Party', {
	// refresh: function(frm) {

	// }
});


frappe.form.link_formatters['Party'] = function(value, doc) {
    return doc.party_name + ' (' + doc.party_type + ')';
}