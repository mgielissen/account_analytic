{
    'name': "Analytic Accounting Structuring",
    'version': '9.0.1.0.0',
    'depends': ['account', 'analytic'],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Accounting',
    'description': 
    """
Account Analytic Account Structured

Manage you analytic accounts in a structured way.

It adds a way to create a hierarchy in the analytic accounts (parents and childs),
this way, new debit, credit and balance fields are set on parents that are sums
of their children's fields.

This module has been developed by Valentin Thirion @ AbAKUS it-solutions
    """,
    'data': [
        'views/account_analytic_account_view.xml',
        'views/account_analytic_line_view.xml',
    ],
}