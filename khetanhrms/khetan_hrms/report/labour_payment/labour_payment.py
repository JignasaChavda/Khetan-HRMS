# Copyright (c) 2023, Jignasha and contributors
# For license information, please see license.txt

from decimal import ROUND_HALF_UP, Decimal
from frappe.utils import flt
import frappe
import calendar
from frappe.utils.xlsxutils import make_xlsx
import csv
from openpyxl import Workbook
from io import BytesIO

def get_month_number(month_name):
    return list(calendar.month_abbr).index(month_name.capitalize()[:3])

def get_employee_holiday_list(employee_id):

    # Fetch the employee's holiday list from the Employee master
    employee = frappe.get_doc("Employee", employee_id)
    return employee.holiday_list

def calculate_total_new_hours(new_hour_values):
    # Calculate total hours without rounding
    total_hours = 0

    for hour in new_hour_values:
        if hour is not None:
            if isinstance(hour, str):  # Handle the case when new_hours is a string
                parts = hour.split('.')
                if parts:
                    hours = int(parts[0]) if parts[0].isdigit() else 0
                    total_hours += hours
            elif isinstance(hour, (int, float)):  # Handle the case when new_hours is a number
                total_hours += int(hour)

    print("\n\n total hours:", total_hours)
    return total_hours

def calculate_total_new_minutes(new_hour_value):

     # Filter out None values and calculate total minutes
    total_minutes = 0
    contributing_minutes = []

    for value in new_hour_value:
        if value is not None:
            if isinstance(value, str) and '.' in value:
                parts = value.split('.')
                if len(parts) == 2 and parts[1].isdigit():
                    # Extract the value after the decimal point
                    minutes_value = int(parts[1])
                    contributing_minutes.append((value, minutes_value))
                    total_minutes += minutes_value

    total_minutes_as_string = str(int(total_minutes))
    return total_minutes_as_string



def calculate_total_new_minutes_for_row(new_hours):
    # Filter out None values and calculate total minutes
    total_minutes = 0
    contributing_minutes = []

    for value in new_hours:
        if value is not None:
            if isinstance(value, str) and '.' in value:
                parts = value.split('.')
                if len(parts) == 2 and parts[1].isdigit():
                    # Extract the value after the decimal point
                    minutes_value = int(parts[1])
                    contributing_minutes.append((value, minutes_value))
                    total_minutes += minutes_value

    total_minutes_as_string = str(int(total_minutes))

    return total_minutes_as_string

def round_to_nearest_20(minutes):
    # Initialize the variable with the original value
    rounded_minutes = minutes
    
    if 1 <= minutes <= 15:
        rounded_minutes = 20

    elif 16 <= minutes <= 30:
        rounded_minutes = 25

    elif 31 <= minutes <= 40:
        rounded_minutes = 35

    elif 41 <= minutes:
        rounded_minutes = 60

    return rounded_minutes


def convert_to_hour_minute_format(total_hours, total_minutes):
    if total_hours is not None and total_minutes is not None:
        total_hours = float(total_hours)
        total_minutes = float(total_minutes)

        # Add the extra hours if total_minutes is greater than or equal to 60
        if total_minutes >= 60:
            additional_hours, remaining_minutes = divmod(total_minutes, 60)
            total_hours += additional_hours
            total_minutes = remaining_minutes

        # Extract hours and minutes from the input
        hours, minutes = divmod(total_hours * 60 + total_minutes, 60)

        # Correct the rounding to two decimal places
        formatted_hours = "{}.{}".format(int(hours), int(minutes))

        return formatted_hours
    else:
        return None  # or some default value if needed


def rounded_hours(total_hours):
    if total_hours is not None and '.' in total_hours:
        before_decimal, after_decimal = total_hours.split('.')
        
        # Check if both parts are present
        if before_decimal and after_decimal:
            tot_minutes = int(before_decimal) * 60 + int(after_decimal)
            tot_hours = round(tot_minutes / 60)
            return tot_hours
    return None

def get_employee_daily_rate(employee_id):

    # Fetch the daily rate from the Employee master
    employee = frappe.get_doc("Employee", employee_id)
    return employee.daily_rate if employee.daily_rate else 0


def execute(filters=None):
    # Extract month and year from filters
    month = filters.get("month", "")
    year = int(filters.get("year", 0))
    employee_type_filter = filters.get("employee_type", "")

    # Ensure the month and year are provided
    if not month or not year:
        frappe.msgprint("Please select both month and year.")
        return [], []

    # Construct date range based on the selected month and year
    start_date = frappe.utils.get_datetime(f"{month}-01-{year}")
    end_date = frappe.utils.get_datetime(f"{month}-{calendar.monthrange(year, get_month_number(month))[1]}-{year}")

    # Fetch data from Attendance table with date range filter
    attendance_data = frappe.get_all("Attendance",
                                     filters={"attendance_date": ["between", [start_date, end_date]],"custom_employee_type": employee_type_filter,"docstatus":1},
                                     fields=['employee', 'employee_name', 'attendance_date', 'new_hours'])

    # Group data by employee
    employee_data = {}
    for entry in attendance_data:
        employee_id = entry.employee
        if employee_id not in employee_data:
            employee_data[employee_id] = {
                "employee": entry.employee,
                "employee_name": entry.employee_name,
                "new_hours": {},
                "holidays": []  # Add a list to store holiday information for each employee
            }
        employee_data[employee_id]["new_hours"][entry.attendance_date.day] = entry.new_hours

    # Dynamically generate columns for each day in the selected month
    _, days_in_month = calendar.monthrange(year, get_month_number(month))
    columns = [
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 100
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 300
        }
    ]

    # Add dynamic columns for each day in the selected month
    for day in range(1, days_in_month + 1):
        columns.append({
            "label": f"{day}",
            "fieldname": f"day_{day}_new_hours",
            "fieldtype": "Data",
            "width": 80
        })
    # Add a total_minutes column for each employee
    columns.append({
        "label": "Total Hour",
        "fieldname": "total_hours",
        "fieldtype": "Data",
		# "hidden": 1,
        "width": 100
    })
    # Add a total_minutes column for each employee
    columns.append({
        "label": "Total Minutes",
        "fieldname": "total_minutes",
        "fieldtype": "Data",
        # "hidden": 1,
        "width": 100
    })
    # Add a total_minutes column for each employee
    columns.append({
        "label": "Total Hours",
        "fieldname": "total_new_hours",
        "fieldtype": "Data",
        "width": 100
    })
    columns.append({
        "label": "Rounded Hours",
        "fieldname": "rounded_hours",
        "fieldtype": "Data",
        "width": 100
    })
    columns.append({
        "label": "Total Payment",
        "fieldname": "total_payment",
        "fieldtype": "Data",
        "width": 100
    })
    columns.append({
        "label": "Advance",
        "fieldname": "advance",
        "fieldtype": "Data",
        "allow_on_submit": True,
        "width": 100
    })
    columns.append({
        "label": "Cpn",
        "fieldname": "cpn",
        "fieldtype": "Data",
        "width": 100
    })
    columns.append({
        "label": "Fine",
        "fieldname": "fine",
        "fieldtype": "Data",
        "width": 100
    })
    columns.append({
        "label": "Prv.Bal",
        "fieldname": "previous_balance",
        "fieldtype": "Data",
        "width": 100
    })
    columns.append({
        "label": "Cash Paid",
        "fieldname": "cashpaid",
        "fieldtype": "Data",
        "width": 100
    })
    columns.append({
        "label": "Bank Paid",
        "fieldname": "cashpaid",
        "fieldtype": "Data",
        "width": 100
    })
    columns.append({
        "label": "Balance",
        "fieldname": "balance",
        "fieldtype": "Data",
        "width": 100
    })
    columns.append({
        "label": "Rate",
        "fieldname": "rate",
        "fieldtype": "Data",
        "width": 100
    })

    data = []

    # Populate data with attendance entries
    for employee_id, employee_info in employee_data.items():
        # Get the employee's holiday list
        holiday_list = get_employee_holiday_list(employee_id)

        # Fetch holidays for the selected month
        holidays = frappe.get_all("Holiday",
                                  filters={"parent": holiday_list,
                                           "holiday_date": ["between", [start_date, end_date]]},
                                  fields=["holiday_date"])
        holiday_dates = [holiday.holiday_date.day for holiday in holidays]

        row = {
            "employee": employee_info["employee"],
            "employee_name": employee_info["employee_name"],
        }

       

        # Add new_hours for each day in the row
        for day in range(1, days_in_month + 1):
            day_key = f"day_{day}_new_hours"
            
            # Print each new_hour before setting it into the column
            if day in holiday_dates:
                if day not in employee_info["new_hours"]:
                    new_hour_value = "WO"  # Set "WO" for holidays with no attendance record
                elif employee_info["new_hours"][day] is None:
                    new_hour_value = "0"  # No working hours, set the column to 0
                else:
                    new_hour_value = str(employee_info["new_hours"].get(day, 0))  # Convert to string
            else:
                if employee_info["new_hours"].get(day) is None:
                    new_hour_value = "0"  # No working hours, set the column to 0
                else:
                    new_hour_value = str(employee_info["new_hours"].get(day, 0))  # Convert to string
            

            #  # Apply rounding logic if the value is a decimal
            if '.' in new_hour_value:
             
                # Extract the minutes part
                minutes_value = int(new_hour_value.split('.')[1])

                rounded_minutes = round_to_nearest_20(minutes_value)

                if rounded_minutes == 60:
                    new_hour_value = f"{int(new_hour_value.split('.')[0]) + 1}.0"
                else:
                    new_hour_value = f"{new_hour_value.split('.')[0]}.{rounded_minutes}"

            row[day_key] = new_hour_value
        
        hour_values = [row.get(f"day_{day}_new_hours", 0) for day in range(1, days_in_month + 1)]

        total_new_hours = calculate_total_new_hours(hour_values)
        total_new_minutes = calculate_total_new_minutes(hour_values)
        total_hours = convert_to_hour_minute_format(total_new_hours, total_new_minutes)
        rounding_hours = rounded_hours(total_hours)

        row["total_hours"] = total_new_hours
        row["total_minutes"] = total_new_minutes
        row["total_new_hours"] = total_hours
        row["rounded_hours"] = rounding_hours 

        daily_rate = get_employee_daily_rate(employee_id)
        row["rate"] = daily_rate 
        total_payment = rounding_hours * daily_rate
        row["total_payment"] = total_payment

        data.append(row)

    # Add a row for "Total Hours" at the end
    total_row = {
        "employee_name": "<b>Total</b>",  # You can change this label if needed
        "is_last_row": 1
    }

    # Calculate the sum of hours for each day
    for day in range(1, days_in_month + 1):
        day_key = f"day_{day}_new_hours"
        total_hours_for_day = calculate_total_new_hours([row.get(day_key, 0) for row in data])
        total_minutes_for_day = calculate_total_new_minutes_for_row([row.get(day_key, 0) for row in data])
        total_new_hours_for_day = convert_to_hour_minute_format(total_hours_for_day,total_minutes_for_day)
    
        total_row[day_key] = f"<b>{total_new_hours_for_day}</b>"

    

    # Calculate the total hours for each employee
    total_hours_row = sum((row["total_hours"]) for row in data)
    total_minutes_row = sum(float(row["total_minutes"]) for row in data)
    total_rounded_hours_row = sum(float(row["rounded_hours"]) for row in data)
    total_hour_minute_row = convert_to_hour_minute_format(total_hours_row,total_minutes_row)
    

    total_row["total_hours"] = total_hours_row
    total_row["total_minutes"] = total_minutes_row

    total_row["total_new_hours"] = f"<b>{total_hour_minute_row}</b>"
    total_row["rounded_hours"] = f"<b>{total_rounded_hours_row}</b>"
    
 

    data.append(total_row)


    return columns, data


@frappe.whitelist(allow_guest=True)
def get_excel_data(month, year, employee_type):
    filters = {"month": month, "year": year, "employee_type": employee_type}

    # Call the execute function to get the data
    columns, data = execute(filters)

    # Prepare data for export
    export_data = {
        "columns": columns,
        "data": data
    }

    return export_data
