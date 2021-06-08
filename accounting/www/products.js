frappe.ready(function () {
        $('.add-to-cart').on('click', (e) => {
            if (frappe.session.user === 'Guest') {
                window.location.href = "/login"
            } else {
                var itemName = $(e.currentTarget).data('item-name');
                frappe.call({
                    method: 'accounting.accounting.doctype.sales_invoice.sales_invoice.add_to_cart',
                    args: {
                        'username': frappe.session.user,
                        'item_name': itemName,
                    }
                });
                frappe.show_alert({
                    message:__(itemName + ' added to cart'),
                    indicator:'green'
                }, 4);
            }
        })
    }
)
