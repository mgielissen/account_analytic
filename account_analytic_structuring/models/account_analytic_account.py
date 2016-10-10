from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class account_analytic_account(models.Model):
    _inherit = ['account.analytic.account']

    parent_account_id = fields.Many2one('account.analytic.account', string="Parent Account")
    child_account_ids = fields.One2many('account.analytic.account', 'parent_account_id', string="Children Accounts")

    structured_name = fields.Char(string="Structured name", compute='_computeStructuredName')
    structured_type = fields.Selection([('parent', 'Parent'), ('account', 'Account')], string="Structured Type")

    structured_debit = fields.Monetary(string="Debit", compute="_compute_debit_credit_balance")
    structured_credit = fields.Monetary(string="Credit", compute="_compute_debit_credit_balance")
    structured_balance = fields.Monetary(string="Balance", compute="_compute_debit_credit_balance")

    @api.multi
    def _compute_debit_credit_balance(self):
        for account in self:
            from_date = self._context.get('from_date')
            to_date = self._context.get('to_date')

            if account.structured_type == 'parent':
                d = 0.0
                c = 0.0
                for sub_account in account.child_account_ids:
                    d += sub_account.structured_debit
                    c += sub_account.structured_credit

                account.structured_debit = d
                account.structured_credit = c
                account.structured_balance = c - d

            else:
                analytic_line_obj = self.env['account.analytic.line']
                domain = [('account_id', '=', account.id), ('move_id', '!=', False)]
                if from_date:
                    domain.append(('date', '>=', from_date))
                if to_date:
                    domain.append(('date', '<=', to_date))

                account_amounts = analytic_line_obj.search_read(domain, ['account_id', 'amount'])
                account_ids = set([line['account_id'][0] for line in account_amounts])
                data_debit = {account_id: 0.0 for account_id in account_ids}
                data_credit = {account_id: 0.0 for account_id in account_ids}
                for account_amount in account_amounts:
                    if account_amount['amount'] < 0.0:
                        data_debit[account_amount['account_id'][0]] += account_amount['amount']
                    else:
                        data_credit[account_amount['account_id'][0]] += account_amount['amount']

                account.structured_debit = abs(data_debit.get(account.id, 0.0))
                account.structured_credit = data_credit.get(account.id, 0.0)
                account.structured_balance = account.structured_debit - account.structured_credit

    @api.one
    @api.depends('parent_account_id')
    def _computeStructuredName(self):
        if not self.parent_account_id:
            self.structured_name = self.name
            return self.name

        full_name = self.name
        parent = self.parent_account_id
        while (parent):
            full_name = parent.name + " \ " + full_name
            parent = parent.parent_account_id

        self.structured_name = full_name
        return full_name

    @api.multi
    def print_account_report(self):
        datas = {
            'ids': [self.id],
            'model': 'account.analytic.account',
            'context': self._context,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account_analytic_structuring.analytic_structured_report',
            'datas': datas,
        }
