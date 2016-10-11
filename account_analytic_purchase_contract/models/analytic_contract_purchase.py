# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class account_analytic_purchase(models.Model):
    _inherit = ['account.analytic.account']

    type = fields.Selection([
            ('view','Analytic View'),
            ('normal','Analytic Account'),
            ('contract','Contract or Project'),
            ('template','Template of Contract'),
            ('purchase_contract','Purchase Contract')],
                            string='Type of Account',
                            required=True,
                            help="If you select the View Type, it means you won\'t allow to create journal entries using that account.\n"\
                                  "The type 'Analytic account' stands for usual accounts that you only want to use in accounting.\n"\
                                  "If you select Contract or Project, it offers you the possibility to manage the validity and the invoicing options for this account.\n"\
                                  "The special type 'Template of Contract' allows you to define a template with default data that you can reuse easily.")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
