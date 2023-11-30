// Copyright (c) 2023, Jignasha and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Labour Payment"] = {
    "filters": [
        {
            "fieldname": "month",
            "label": __("Month"),
            "fieldtype": "Select",
            "options": "January\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
            "default": frappe.datetime.get_today().split("-")[1],
            "reqd": 1
        },
        {
            "fieldname": "year",
            "label": __("Year"),
            "fieldtype": "Data",
            "default": frappe.datetime.get_today().split("-")[0],
            "reqd": 1
        }
    ],

};
