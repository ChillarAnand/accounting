// Copyright (c) 2016, ac and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Profit and Loss"] = {
	"filters": [
	    {
	        'fieldname': 'filter_type',
	        'label': 'Filter Type',
	        'fieldtype': 'Select',
	        'options': ['Fiscal Year', 'Date Range'],
	        'default': 'Date Range',
	        on_change: function() {
				let filter_type = frappe.query_report.get_filter_value('filter_type');
				frappe.query_report.toggle_filter_display('fiscal_year', filter_type === 'Date Range');
				frappe.query_report.toggle_filter_display('from_date', filter_type === 'Fiscal Year');
				frappe.query_report.toggle_filter_display('to_date', filter_type === 'Fiscal Year');
				frappe.query_report.refresh();
			}

	    },
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"fiscal_year",
			"label": __("Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"width": "60px",
			"hidden": 1,
		}
	],

	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && !data.parent_account) {
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}
		return value;
	},
};
