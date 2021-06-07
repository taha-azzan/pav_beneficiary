# -*- coding: utf-8 -*-
# Copyright (c) 2021, Taha Azzan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate
from pav_beneficiary.beneficiary.utils import update_beneficiary



class BeneficiaryModification(Document):
	def validate(self):
		if frappe.get_value("Beneficiary", self.beneficiary, "status") == "Canceled":
			frappe.throw(_("Cannot modification Beneficiary with status Canceled"))

	def before_submit(self):
		if getdate(self.modification_date) > getdate():
			frappe.throw(_("Beneficiary Modification cannot be submitted before Modification Date "),
				frappe.DocstatusTransitionError)

	def on_submit(self):
		beneficiary = frappe.get_doc("Beneficiary Data", self.beneficiary)
		beneficiary = update_beneficiary(beneficiary, self.beneficiary_modification_details, date=self.modification_date)
		beneficiary.save()

	def on_cancel(self):
		beneficiary = frappe.get_doc("Beneficiary Data", self.beneficiary)
		beneficiary = update_beneficiary(beneficiary, self.beneficiary_modification_details, cancel=True)
		beneficiary.save()