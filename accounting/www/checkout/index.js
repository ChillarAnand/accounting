frappe.ready(function () {
    $('.buy-now').on('click', (e) => {
        frappe.call({
            method: 'accounting.accounting.doctype.sales_invoice.sales_invoice.buy_now',
            args: {
                'invoice_name': $(e.currentTarget).data('invoice-name'),
            }
        })
        window.location.href = "/orders";
    })
})
