from openerp import models, fields

class account_analytic_line_improvements(models.Model):
    _inherit = ['account.analytic.line']

    on_site = fields.Boolean(string="On site", help="Check this box if the work has not been done at Service Desk but On Site (by the Customer)", default=False)