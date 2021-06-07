# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, erpnext
from frappe import _
from frappe.utils import formatdate, format_datetime, getdate, get_datetime, nowdate, flt, cstr, add_days, today
from frappe.model.document import Document
#from pav_beneficiary.beneficiary.doctype.beneficiary_data.beneficiary_data

class DuplicateDeclarationError(frappe.ValidationError): pass

def set_beneficiary_name(doc):
	if doc.beneficiary and not doc.beneficiary_data:
		doc.beneficiary_data = frappe.db.get_value("Beneficiary Data", doc.beneficiary, "beneficiary_data")

def update_beneficiary(beneficiary, details, date=None, cancel=False):
        internal_work_history = {}
        for item in details:
            fieldtype = frappe.get_meta("Beneficiary Data").get_field(item.fieldname).fieldtype
            new_data = item.new if not cancel else item.current
            if fieldtype == "Date" and new_data:
                new_data = getdate(new_data)
            elif fieldtype =="Datetime" and new_data:
                new_data = get_datetime(new_data)
            setattr(beneficiary, item.fieldname, new_data)
            if item.fieldname in ["department", "designation", "branch"]:
                internal_work_history[item.fieldname] = item.new
        if internal_work_history and not cancel:
            internal_work_history["from_date"] = date
            employee.append("internal_work_history", internal_work_history)
        return beneficiary

@frappe.whitelist()
def get_beneficiary_fields_label():
	fields = []
	for df in frappe.get_meta("Beneficiary Data").get("fields"):
		if df.fieldname in ["age", "health_status", "social_status", "financial_status",
			"job", "type_of_housing", "address", "no_of_family_members", "responsible_opinion",
			"assistance_amount", "recommendations", "assistance_frequency"]:
				fields.append({"value": df.fieldname, "label": df.label})
	return fields

@frappe.whitelist()
def get_beneficiary_field_property(beneficiary, fieldname):
	if beneficiary and fieldname:
		field = frappe.get_meta("Beneficiary Data").get_field(fieldname)
		value = frappe.db.get_value("Beneficiary Data", beneficiary, fieldname)
		options = field.options
		if field.fieldtype == "Date":
			value = formatdate(value)
		elif field.fieldtype == "Datetime":
			value = format_datetime(value)
		return {
			"value" : value,
			"datatype" : field.fieldtype,
			"label" : field.label,
			"options" : options
		}
	else:
		return False