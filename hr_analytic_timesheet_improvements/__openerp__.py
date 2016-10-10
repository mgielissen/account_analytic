{
    'name': "Worklog management improvements",
    'version': '9.0.1.0.0',
    'depends': ['hr_timesheet',
                'project_timesheet',
                'project_issue_sheet'],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Humain Resources',
    'description': 
    """
    Worklog management improvements
        
        - It add a calendar view for the worklogs.
        - date_begin is a new datetime field used to order the
        worklogs in the calendar. This field is created because
        the date field from the worklog is a standard date type
        and we need hours and minutes.
        - It changes the security rule for multi-company
        (Analytic Line, Timesheet allowed in read)

    This module has been developed by
    Bernard DELHEZ @ AbAKUS it-solution.
    """,
    'data': ['view/hr_analytic_timesheet_view.xml',
             'view/project_issue_view.xml',
             'view/hr_timesheet_sheet_view.xml',
             'hr_analytic_timesheet_data.xml',
            ],
}
