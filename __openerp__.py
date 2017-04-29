# -*- coding: utf-8 -*-
{
    'name': "sale_investments",

    'summary': """
        Extension of sales module to accomodate sale of properties to investors""",

    'description': """
        This is an extension to allow investors purchase land, track payment for those properties
        over time and penalize defaulters for late payment. Also provides functionality for purchase,
        subdivision and allocation of costs to be included in cost of sales for properties. Maintains
        an investor register and allows registration of investors
    """,

    'author': "Tritel Technologies",
    'website': "http://www.tritel.co.ke",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Investment',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','tritel'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/wizards.xml',
        'views/investment_views.xml',

        'views/sequences.xml',
        'views/product.xml',
        'views/partner.xml',
        'data/scheduler.xml',
        'views/account_invoice.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
