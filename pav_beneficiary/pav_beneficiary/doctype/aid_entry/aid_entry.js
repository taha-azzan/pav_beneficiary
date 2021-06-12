// Copyright (c) 2020, Akram Mutaher and contributors
// For license information, please see license.txt

frappe.ui.form.on('AID Entry', {
	refresh: function(frm) {
		frm.set_df_property("get_beneficiary", "hidden", frm.doc.__islocal ? 1:0);
	
		if (frm.doc.docstatus == 1) {
			frm.events.add_context_buttons(frm);
		}
	},

	add_context_buttons: function(frm) {
			frm.add_custom_button(__("Submit AID Log"), function() {
			frm.add_custom_button(__("Submit AID Log"), function() {	
			}).addClass("btn-primary");	
			}).addClass("btn-primary");
	},

	get_beneficiary: function(frm){
		frm.events.fill_beneficiary(frm);
	},

	fill_beneficiary: function (frm) {
		return frappe.call({
			doc: frm.doc,
			method: 'fill_beneficiary',
			callback: function(r) {
				if (r.docs[0].beneficiaries){
					frm.save();
					frm.refresh();
				}
			}
		})
	}
});

frappe.ui.form.on('AID Entry', {
	setup: function(frm) {
    	frm.fields_dict['beneficiaries'].grid.get_field('beneficiary').get_query = function(frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			return{
				filters: {
					"type": frm.type
				}
			}
	    }	   
	}
})


frappe.ui.form.on('AID Entry', {
	refresh(frm) {
	cur_frm.set_query("beneficiary", "beneficiaries", function(doc, cdt, cdn) {
	    var d = locals[cdt][cdn];
    	return{
	    	filters: [
		    
		    	['Beneficiary Data', 'type', '=', d.type]
	    	]
            	}
        });
	}
})
