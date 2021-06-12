# -*- coding: utf-8 -*-
# Copyright (c) 2020, Akram Mutaher and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class AIDEntry(Document):
	def validate(self):
		self.sort_details()
	def on_submit(self):
		self.create_logs()

	def get_existing_beneficiary_list(self):
		"""
			Returns list of active beneficiary based on selected criteria
			and for which type exists
		"""
		return frappe.db.sql_list("""select beneficiary as beneficiary from `tabAID Entry Details` 
		where parentfield='beneficiaries' and parent=%s order by beneficiary ASC""",self.name)

	def get_beneficiary_list(self):
		"""
			Returns list of active beneficiaries based on selected criteria
			and for which type exists
		"""
		# cond =''
		cond = self.get_filter_condition()
		# cond += self.get_joining_relieving_condition()

		# condition = ''
				
		cond += "and %(from_date)s >= t2.from_date"
		emp_list = frappe.db.sql("""
			select
				distinct t1.name as beneficiary, t1.beneficiary_name, t2.assistance_type
			from
				`tabBeneficiary Data` t1, `tabAID Assignment` t2
			where
				t1.name = t2.beneficiary
				and t2.docstatus = 1
		%s order by t2.from_date desc
		""" % cond, {"from_date": self.posting_date}, as_dict=True)
		frappe.msgprint("{0}".format(emp_list))
		return emp_list
		# return frappe.db.sql("""select ac.name as beneficiary, ac.beneficiary_name as beneficiary_name from `tabBeneficiary Data` ac 
		# where ac.type=%s and ac.assistance_frequency=%s """,[self.type, self.assistance_frequency], as_dict=True)
	
	def get_filter_condition(self):
		self.check_mandatory()

		cond = ''
		for f in ['governorate', 'district']:
			if self.get(f):
				cond += " and t1." + f + " = '" + self.get(f).replace("'", "\'") + "'"
				
		for f in ['assistance_type', 'assistance_frequency']:
			if self.get(f):
				cond += " and t2." + f + " = '" + self.get(f).replace("'", "\'") + "'"

		return cond
	
	# def get_joining_relieving_condition(self):
	# 	cond = """
	# 		and ifnull(t1.date_of_joining, '0000-00-00') <= '%(end_date)s'
	# 		and ifnull(t1.relieving_date, '2199-12-31') >= '%(start_date)s'
	# 	""" % {"start_date": self.start_date, "end_date": self.end_date}
	# 	return cond
	
	def check_mandatory(self):
		for fieldname in ['posting_date']:
			if not self.get(fieldname):
				frappe.throw(_("Please set {0}").format(self.meta.get_label(fieldname)))

	def fill_beneficiary(self):			
		#self.set('work_plan_details', [])
		beneficiaries = self.get_beneficiary_list()
		if not beneficiaries:
			frappe.throw(_("No beneficiaries for the mentioned type"))
		existing_beneficiaries=self.get_existing_beneficiary_list()
		for d in beneficiaries:
			if d.beneficiary not in existing_beneficiaries:
				self.append('beneficiaries', d)
		
		self.number_of_beneficiaries = len(beneficiaries)
		#self.sort_details()

	def sort_details(self):
		#enumerate # built-in function that return a list of (index, item) of a given list of objects), `start` is a parameter to define the first value of the index
		#sorted # built-in function that sort a list, if the list is a list of objects, do you need pass the `key` to get the value to be used in the sort comparization.
		for i, item in enumerate(sorted(self.beneficiaries, key=lambda item: item.beneficiary), start=1):
			item.idx = i # define the new index to the object based on the sorted ordem



	# def create_logs(self):
	# 	if self.beneficiaries:
	# 		for m in self.get("beneficiaries"):
	# 			log_args = frappe._dict({
	# 				"doctype": "AID Log",
	# 				"aid_entry": self.name,
	# 				"tpye": self.type,
	# 				"beneficiary": m.beneficiary,
	# 				"aid_period": self.aid_period,
	# 			})
	# 			il = frappe.get_doc(log_args)
	# 			il.insert()

	# def get_existing_aid_logs(self):
	# 	logs = frappe.db.sql("""
	# 		select docstatus from `tabAID Log`
	# 		where parent = %s
	# 	""", [self.name], as_dict = True)
	
	def create_logs(self):
		"""
			Creates salary slip for selected employees if already not created
		"""
		self.check_permission('write')
		self.created = 1
		emp_list = [d.beneficiary for d in self.get_beneficiary_list()]
		if emp_list:
			args = frappe._dict({
				"doctype": "AID Log",
				"aid_entry": self.name,				
				"posting_date": self.posting_date
			})
			if len(emp_list) > 30:
				frappe.enqueue(create_salary_slips_for_employees, timeout=600, employees=emp_list, args=args)
			else:
				create_salary_slips_for_employees(emp_list, args, publish_progress=False)
				# since this method is called via frm.call this doc needs to be updated manually
				self.reload()

def create_salary_slips_for_employees(employees, args, publish_progress=True):
	salary_slips_exists_for = get_existing_salary_slips(employees, args)
	count=0
	for emp in employees:
		if emp not in salary_slips_exists_for:
			args.update({
				"beneficiary": emp
			})
			ss = frappe.get_doc(args)
			ss.insert()
			count+=1
			if publish_progress:
				frappe.publish_progress(count*100/len(set(employees) - set(salary_slips_exists_for)),
					title = _("Creating Salary Slips..."))

	payroll_entry = frappe.get_doc("AID Entry", args.aid_entry)
	payroll_entry.db_set("aid_logs_created", 1)
	payroll_entry.notify_update()

def get_existing_salary_slips(employees, args):
	return frappe.db.sql_list("""
		select distinct beneficiary from `tabAID Log`
		where docstatus!= 2 
			and posting_date = %s
			and beneficiary in (%s)
	""" % ('%s', ', '.join(['%s']*len(employees))),
		[args.posting_date] + employees)