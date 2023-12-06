# Copyright (c) 2023, Jignasha and contributors
# For license information, please see license.txt


import frappe
import json
from frappe.model.document import Document

@frappe.whitelist(allow_guest=True)
def get_employee_data(category):


	# Fetch Employee details based on the given category
	emp_details = frappe.get_all("Employee", filters={"status": "Active", "employee_type": category},
								fields=['employee', 'employee_name', 'daily_rate', 'employee_type'], order_by="idx Asc")
	return emp_details

class LabourPaymentUpload(Document):
	pass
    
