// Copyright (c) 2021, ac and contributors
// For license information, please see license.txt

frappe.ui.form.on('Account', {
	setup: function(frm) {
        frm.set_query('parent_account', function (){
            return {
                'filters': {
                    'is_group': 1,
                }
            }
        })
	}
});
