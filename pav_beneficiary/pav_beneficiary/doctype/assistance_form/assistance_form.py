# -*- coding: utf-8 -*-
# Copyright (c) 2021, Taha Azzan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AssistanceForm(Document):
	def on_submit(self):
		benf = frappe.get_all('Beneficiary Data', filters={'assistance_form': self.name})
		if not benf and self.status=="Approved" and self.auto_create_after_submit:
			frappe.get_doc(dict(
					doctype = 'Beneficiary Data',
					assistance_form = self.name,
			)).insert()