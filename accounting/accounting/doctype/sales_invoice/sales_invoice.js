// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt


//frappe.ui.form.on("Sales Invoice", {
//	setup: function(frm) {
//		frm.set_query("party", function() {
//			return {
//				filters: [
//					["Party", "party_type", "=", "Customer"]
//				]
//			}
//		});
//	}
//});


frappe.ui.form.on("Sales Invoice", "onload", function(frm) {
    frm.set_query("party", function() {
        return {
            "filters": {
                "party_type": "Customer"
            }
        };
    });
});