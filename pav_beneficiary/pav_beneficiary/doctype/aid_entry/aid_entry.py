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
		return frappe.db.sql("""select ac.name as beneficiary, ac.beneficiary_name as beneficiary_name from `tabBeneficiary Data` ac 
		where ac.type=%s and ac.assistance_frequency=%s """,[self.type, self.assistance_frequency], as_dict=True)

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



	def create_logs(self):
		if self.beneficiaries:
			for m in self.get("beneficiaries"):
				log_args = frappe._dict({
					"doctype": "AID Log",
					"aid_entry": self.name,
					"tpye": self.type,
					"beneficiary": m.beneficiary,
					"aid_period": self.aid_period,
				})
				il = frappe.get_doc(log_args)
				il.insert()