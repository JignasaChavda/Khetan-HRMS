// Copyright (c) 2023, Jignasha and contributors
// For license information, please see license.txt


frappe.ui.form.on('Labour Payment Upload', {
    get_data: function(frm) {
        frm.call({
            method: 'khetanhrms.khetan_hrms.doctype.labour_payment_upload.labour_payment_upload.get_employee_data',
            args: {
                category: frm.doc.category
            },
            callback: function(response) {
                if (response.message) {
					frm.clear_table('employee_details');
                    $.each(response.message, function(i, data) {
                        var row = frappe.model.add_child(cur_frm.doc, 'Labours Payment Upload Sheet', 'employee_details');
						row.employee = data.employee;
                        row.employee_name = data.employee_name;
						row.employee_type = data.employee_type;
						
                       
                    });
                    frm.refresh_field('employee_details');
                   
                }

            }
        });
    },
});