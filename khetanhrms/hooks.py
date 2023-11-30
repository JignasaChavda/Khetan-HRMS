from . import __version__ as app_version

app_name = "khetanhrms"
app_title = "Khetan HRMS"
app_publisher = "Jignasha"
app_description = "Khetan HRMS"
app_email = "jignasha@sanskartechnolab.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/khetanhrms/css/khetanhrms.css"
# app_include_js = "/assets/khetanhrms/js/khetanhrms.js"

# include js, css files in header of web template
# web_include_css = "/assets/khetanhrms/css/khetanhrms.css"
# web_include_js = "/assets/khetanhrms/js/khetanhrms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "khetanhrms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "khetanhrms.utils.jinja_methods",
#	"filters": "khetanhrms.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "khetanhrms.install.before_install"
# after_install = "khetanhrms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "khetanhrms.uninstall.before_uninstall"
# after_uninstall = "khetanhrms.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "khetanhrms.utils.before_app_install"
# after_app_install = "khetanhrms.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "khetanhrms.utils.before_app_uninstall"
# after_app_uninstall = "khetanhrms.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "khetanhrms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Employee Checkin": "khetanhrms.employee_checkin_overrides.EmployeeCheckin",
    "Employee": "khetanhrms.employee_overrides.Employee"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"khetanhrms.tasks.all"
#	],
#	"daily": [
#		"khetanhrms.tasks.daily"
#	],
#	"hourly": [
#		"khetanhrms.tasks.hourly"
#	],
#	"weekly": [
#		"khetanhrms.tasks.weekly"
#	],
#	"monthly": [
#		"khetanhrms.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "khetanhrms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "khetanhrms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "khetanhrms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["khetanhrms.utils.before_request"]
# after_request = ["khetanhrms.utils.after_request"]

# Job Events
# ----------
# before_job = ["khetanhrms.utils.before_job"]
# after_job = ["khetanhrms.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------


# auth_hooks = [
#	"khetanhrms.auth.validate"
# ]
fixtures = [
    {"dt":"Custom Field","filters":[
        [
            "module","in",[
                "Khetan HRMS"
            ]
        ]
    ]},
    {"dt":"Property Setter","filters":[
        [
            "module","in",[
                "Khetan HRMS"
            ]
        ]
    ]},
    {"dt":"Client Script","filters":[
        [
            "module","in",[
                "Khetan HRMS"
            ]
        ]
    ]},
    {"dt":"Report","filters":[
        [
            "module","in",[
                "Khetan HRMS"
            ]
        ]
    ]},
    {"dt":"Role","filters":[
        [
            "name","in",[
                "Employee Creator"
            ]
        ]
    ]},
    {"dt":"Custom DocPerm","filters":[
        [
            "name","in",[
                "1c8ad451db"
            ]
        ]
    ]},

]