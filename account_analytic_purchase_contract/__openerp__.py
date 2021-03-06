# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Account Analytic Purchase Contract",
    'version': '9.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Quotations, Sales Orders, Invoicing',
    'description': """
Account Analytic Purchase Contract
==================================
Manage Purchase Contracts and generate Recurring Invoices as you can do in
sales.
    """,
    'author':  'ADHOC SA & AbAKUS it-solutions',
    'website': 'www.adhoc.com.ar & www.abakusitsolutions.eu',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'sale_contract',
        'purchase',
    ],
    'data': [
        'views/account_purchase_contract_view.xml',
        'views/account_purchase_contract_menu.xml',
        'data/account_analytic_analysis_cron.xml'
    ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
