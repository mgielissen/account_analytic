{
    'name': "AbAKUS OS/SD contract improvements",
    'version': '9.0.1.1.0',
    'depends': [
                'hr_timesheet_sheet',
                'project_issue',
                'project_issue_sheet',
                ],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Contract',
    'description': """This modules the on site management for contract timesheets activities for AbAKUS.
    
This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.""",
    'data': ['views/sale_subscription_view.xml',
             'views/hr_analytic_timesheet_view.xml',
             'views/project_issue_view.xml',
             'views/account_analytic_line.xml',
             'views/hr_timesheet_sheet_view.xml',
             'views/project_task_view.xml',
    ],
}
