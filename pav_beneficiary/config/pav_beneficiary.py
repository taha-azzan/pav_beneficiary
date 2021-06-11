from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Beneficiary"),
			"items": [
				{
					"type": "doctype",
					"name": "Beneficiary Data",
					"doctype": "Beneficiary Data",
				},
			]
		},

	]