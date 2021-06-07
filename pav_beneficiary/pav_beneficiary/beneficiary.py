from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Assistance Details"),
			"items": [
				{
					"type": "doctype",
					"name": "Assistance Request",
					"description":_("Assistance Request"),
                    "dependencies": ["Assistance Type"],
				},
				{
					"type": "doctype",
					"name": "Assistance Form",
					"description":_("Assistance Form"),
					"onboard": 1,
					"dependencies": ["Assistance Request"],
				},
                {
					"type": "doctype",
					"name": "Beneficiary Data",
					"description":_("Beneficiary Data"),
					"onboard": 1,
					"dependencies": ["Assistance Form"],
				},
                {
					"type": "doctype",
					"name": "Assistance Type",
					"description":_("Assistance Type"),
				},
			]
		},
		{
			"label": _("AID Details"),
			"items": [
				{
					"type": "doctype",
					"name": "AID Log",
					"description":_("AID Log"),
					"onboard": 1,
					"dependencies": ["Beneficiary Data"],
				},
				{
					"type": "doctype",
					"name": "AID Entry",
					"description":_("AID Entry"),
				},
			]
		},
		{
			"label": _("Annual Evaluation Details"),
			"items": [
				{
					"type": "doctype",
					"name": "Annual Evaluation Form",
					"description":_("Annual Evaluation Form"),
					"onboard": 1,
					"dependencies": ["Beneficiary"],
				},
			]
		},
	]