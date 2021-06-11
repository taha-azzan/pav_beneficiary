// Copyright (c) 2021, Taha Azzan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Assignment Form", "validate", function(frm) {
    if (frm.doc.from_date > frm.doc.to_date){
           frappe.msgprint(__("To Date Greater than From Date"));
           frappe.validated = false;
       }
       else
       frappe.validated = true;
		// your code here
    
});


