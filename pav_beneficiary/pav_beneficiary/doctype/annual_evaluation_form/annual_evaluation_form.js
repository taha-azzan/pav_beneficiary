frappe.ui.form.on("Annual Evaluation Form", {
	refresh: function(frm) {
		// make calculation on the fields
		var total = frm.doc.male_no + frm.doc.female_no;
		frm.set_value("total_family_members", total);
		frm.refresh_field("total_family_members");
	}
});



frappe.ui.form.on('Annual Evaluation Form', {

beneficiary_data: function(frm) {
   

	frappe.call({
		"method": "frappe.client.get",
		args: {
			doctype: "Beneficiary Data",
			name: frm.doc.beneficiary_data
		},
		callback: function(data){
			frm.fields_dict.family_members.grid.remove_all();
			let family_members = data.message.family_members;
			for (var i in family_members) {
				frm.add_child("family_members");
				frm.fields_dict.family_members.get_value()[i].name1 = family_members[i].name1;
				frm.fields_dict.family_members.get_value()[i].age = family_members[i].age;
				frm.fields_dict.family_members.get_value()[i].educational_level = family_members[i].educational_level;
				frm.fields_dict.family_members.get_value()[i].family_rehabilitation = family_members[i].family_rehabilitation;
				frm.fields_dict.family_members.get_value()[i].able_to_work = family_members[i].able_to_work;
				frm.fields_dict.family_members.get_value()[i].average_monthly_income = family_members[i].average_monthly_income;
				frm.fields_dict.family_members.get_value()[i].average_daily_income = family_members[i].average_daily_income;
			}
			frm.refresh();
			grid_row.toggle_editable("family_members", 0);
		}
	});

},

});






frappe.ui.form.on('Annual Evaluation Form', {

beneficiary_data: function(frm) {
   

	frappe.call({
		"method": "frappe.client.get",
		args: {
			doctype: "Beneficiary Data",
			name: frm.doc.beneficiary_data
		},
		callback: function(data){
			frm.fields_dict.house_details.grid.remove_all();
			let house_details = data.message.house_details;
			for (var ii in house_details) {
				frm.add_child("house_details");
				frm.fields_dict.house_details.get_value()[ii].status = house_details[ii].status;
				frm.fields_dict.house_details.get_value()[ii].rate = house_details[ii].rate;
				frm.fields_dict.house_details.get_value()[ii].description = house_details[ii].description;
			}
			frm.refresh();
			grid_row.toggle_editable("house_details", 1);
		}
	});

},

});    