frappe.ready(function (){
    $('.download-invoice').on(click, (e) => {
        frappe.call({
            method: '/api/method/frappe.utils.'
        })
    })
})
