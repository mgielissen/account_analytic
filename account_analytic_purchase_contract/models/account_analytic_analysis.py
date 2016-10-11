# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from dateutil.relativedelta import relativedelta
import datetime
import time
import logging
_logger = logging.getLogger(__name__)

from openerp import models, fields, api
import openerp.tools
from openerp.tools.translate import _
from openerp.exceptions import UserError

from openerp.addons.decimal_precision import decimal_precision as dp


class purchase_subscription(models.Model):
    _inherit = "sale.subscription"

    type = fields.Selection([('contract', 'Sale Contract'), ('template', 'Template'), ('purchase_contract', 'Purchase Contract')], string='Type')

    def _prepare_purchase_invoice_data(self, cr, uid, contract, context=None):
        context = context or {}

        journal_obj = self.pool.get('account.journal')
        if contract.type == 'purchase_contract':
            invoice = {}
            if not contract.partner_id:
                raise osv.except_osv(_('No Supplier Defined!'), _(
                    "You must first select a Supplier for Contract %s!") % contract.name)

            fpos = contract.partner_id.property_account_position_id or False
            journal_ids = journal_obj.search(cr, uid, [(
                'type', '=', 'purchase'), ('company_id', '=', contract.company_id.id or False)], limit=1)
            if not journal_ids:
                raise osv.except_osv(_('Error!'),
                                     _('Please define a pruchase journal for the company "%s".') % (contract.company_id.name or '', ))

            currency_id = False
            if contract.pricelist_id:
                currency_id = contract.pricelist_id.currency_id.id
            elif contract.partner_id.property_product_pricelist:
                currency_id = contract.partner_id.property_product_pricelist.currency_id.id
            elif contract.company_id:
                currency_id = contract.company_id.currency_id.id

            invoice = {
                'account_id': contract.partner_id.property_account_payable_id.id,
                'type': 'in_invoice',
                'reference': contract.name,
                'partner_id': contract.partner_id.id,
                'currency_id': currency_id,
                'journal_id': len(journal_ids) and journal_ids[0] or False,
                'date_invoice': contract.recurring_next_date,
                'origin': contract.code,
                'fiscal_position_id': fpos and fpos.id,
                'company_id': contract.company_id.id or False,
            }
            return invoice
        else:
            return super(purchase_subscription, self)._prepare_purchase_invoice_data(cr, uid, contract, context=context)

    def _prepare_purchase_invoice_lines(self, cr, uid, contract, fiscal_position_id, context=None):
        if not context:
            context = {}
        if contract.type == 'purchase_contract':
            fpos_obj = self.pool.get('account.fiscal.position')
            fiscal_position = None
            if fiscal_position_id:
                fiscal_position = fpos_obj.browse(
                    cr, uid,  fiscal_position_id, context=context)
            invoice_lines = []
            for line in contract.recurring_invoice_line_ids:

                res = line.product_id
                account_id = res.property_account_expense_id.id
                if not account_id:
                    account_id = res.categ_id.property_account_expense_categ_id.id
                account_id = fpos_obj.map_account(
                    cr, uid, fiscal_position, account_id)

                taxes = res.supplier_taxes_id or False
                if taxes:
                    tax_ids = [x.id for x in taxes]
                    tax_ids = self.pool['account.tax'].search(
                        cr, uid,
                        [('id', 'in', tax_ids), ('company_id', '=', contract.company_id.id)],
                        context=context)
                    taxes = self.pool['account.tax'].browse(cr, uid, tax_ids, context=context)
                tax_id = fpos_obj.map_tax(cr, uid, fiscal_position, taxes)

                invoice_lines.append((0, 0, {
                    'name': line.name,
                    'account_id': account_id,
                    'account_analytic_id': contract.analytic_account_id.id,
                    'price_unit': line.price_unit or 0.0,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id or False,
                    'product_id': line.product_id.id or False,
                    'invoice_line_tax_ids': [(6, 0, tax_id)],
                }))
            return invoice_lines
        else:
            return super(purchase_subscription, self)._prepare_purchase_invoice_lines(cr, uid, contract, fiscal_position_id, context=None)

    def _prepare_purchase_invoice(self, cr, uid, contract, context=None):
        invoice = self._prepare_purchase_invoice_data(cr, uid, contract, context=context)
        invoice['invoice_line_ids'] = self._prepare_purchase_invoice_lines(cr, uid, contract, invoice['fiscal_position_id'], context=context)
        return invoice

    def _recurring_create_purchase_invoice(self, cr, uid, ids, automatic=False, context=None):
        context = context or {}
        invoice_ids = []
        current_date = time.strftime('%Y-%m-%d')
        if ids:
            contract_ids = ids
        else:
            contract_ids = self.search(cr, uid, [('recurring_next_date', '<=', current_date), ('state', '=', 'open'), ('type', '=', 'purchase_contract')])
        if contract_ids:
            cr.execute('SELECT a.company_id, array_agg(sub.id) as ids FROM sale_subscription as sub JOIN account_analytic_account as a ON sub.analytic_account_id = a.id WHERE sub.id IN %s GROUP BY a.company_id', (tuple(contract_ids),))
            for company_id, ids in cr.fetchall():
                context_company = dict(context, company_id=company_id, force_company=company_id)
                for contract in self.browse(cr, uid, ids, context=context_company):
                    try:
                        invoice_values = self._prepare_purchase_invoice(cr, uid, contract, context=context_company)
                        invoice_ids.append(self.pool['account.invoice'].create(cr, uid, invoice_values, context=context_company))
                        self.pool['account.invoice'].compute_taxes(cr, uid, [invoice_ids[-1]], context=context_company)
                        next_date = datetime.datetime.strptime(contract.recurring_next_date or current_date, "%Y-%m-%d")
                        interval = contract.recurring_interval
                        if contract.recurring_rule_type == 'daily':
                            new_date = next_date + relativedelta(days=+interval)
                        elif contract.recurring_rule_type == 'weekly':
                            new_date = next_date + relativedelta(weeks=+interval)
                        elif contract.recurring_rule_type == 'monthly':
                            new_date = next_date + relativedelta(months=+interval)
                        else:
                            new_date = next_date + relativedelta(years=+interval)
                        self.write(cr, uid, [contract.id], {'recurring_next_date': new_date.strftime('%Y-%m-%d')}, context=context_company)
                        if automatic:
                            cr.commit()
                    except Exception:
                        if automatic:
                            cr.rollback()
                            _logger.exception('Fail to create recurring invoice for contract %s', contract.code)
                        else:
                            raise
        return invoice_ids

    def _cron_recurring_create_invoice_purchase(self, cr, uid, context=None):
        return self._recurring_create_purchase_invoice(cr, uid, [], automatic=True, context=context)

    def action_subscription_invoice(self, cr, uid, ids, context=None):
        subs = self.browse(cr, uid, ids, context=context)
        analytic_ids = [sub.analytic_account_id.id for sub in subs]
        orders = self.pool['sale.order'].search_read(cr, uid, domain=[('subscription_id', 'in', ids)], fields=['name'], context=context)
        order_names = [order['name'] for order in orders]
        invoice_ids = self.pool['account.invoice'].search(cr, uid, ['|', ('invoice_line_ids.account_analytic_id', 'in', analytic_ids), ('origin', 'in', [sub.code for sub in subs] + order_names)], context=context)
        imd = self.pool['ir.model.data']
        list_view_id = imd.xmlid_to_res_id(cr, uid, 'account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id(cr, uid, 'account.invoice_form')
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.invoice",
            "views": [[list_view_id, "tree"], [form_view_id, "form"]],
            "domain": [["id", "in", invoice_ids]],
            "context": {"create": False},
            "name": _("Invoices"),
        }
