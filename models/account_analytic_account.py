from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class account_analytic_account(models.Model):
     _inherit = ['account.analytic.account']