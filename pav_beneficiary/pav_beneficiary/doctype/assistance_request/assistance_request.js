frappe.ui.form.on('Assistance Request', {
	refresh(frm) {
	    console.log("in refresh");
            //cur_frm.set_value(age, moment().diff(dob, 'years'));
            //cur_frm.refresh_field(age)
            // your code here
	},
	age: function(frm){
	    if(frm.doc.age){
	        let d=new Date(get_today());
	        cur_frm.set_value("dob",(d.getFullYear()-frm.doc.age)+"-01-01");
	    }
	},
	
	
	/*age_type: function(frm){
	    if(frm.doc.age>=30 && frm.doc.age_date=="year"){
	        frm.set_value("age_type", "Adult");
	    }
	},
	validate(frm){
	    frm.trigger("age_type");
	},*/
});



frappe.ui.form.on('Assistance Request', {
	refresh: function (frm) {
		
	},
	onload: function (frm) {
		if(frm.doc.dob){
			$(frm.fields_dict['age_html'].wrapper).html("AGE : " + get_age(frm.doc.dob));
		}
	}
});







/*frappe.ui.form.on('Assistance Request', {
	refresh: function (frm) {
		
	},
	onload: function (frm) {
		if(frm.doc.dob){
			$(frm.fields_dict['age_html'].wrapper).html("AGE : " + get_age(frm.doc.dob));
		}
	}
});

frappe.ui.form.on("Assistance Request", "dob", function(frm) {
	if(frm.doc.dob){
		var today = new Date();
		var birthDate = new Date(frm.doc.dob);
		var age_str = get_age(frm.doc.dob);
		$(frm.fields_dict['age_html'].wrapper).html("AGE : " + age_str);
	}
});

var get_age = function (birth) {
	var ageMS = Date.parse(Date()) - Date.parse(birth);
	var age = new Date();
	age.setTime(ageMS);
	var years = age.getFullYear() - 1970;
	return years + " Year(s) " + age.getMonth() + " Month(s) " + age.getDate() + " Day(s)";
};*/





frappe.ui.form.on('Assistance Request', {
	refresh(frm) {
		if (frm.doc.docstatus==1){
			frm.add_custom_button(__("Assistance Form"),
				() => frm.events.make_form(frm), __('Create'));
		}	
		
	},
	make_form: function(frm) {
		frappe.route_options = {
		    "assistance_request": frm.doc.name,
		    
		},
		frappe.set_route("Form", 'Assistance Form', 'New Assistance Form');

	},
	
});