# -*- coding: utf-8 -*-
{
    'name' : 'Invoicing Dates for Sale Order Lines',
    'version' : '1.0',
    'summary': 'Custom invoice',
    'sequence': 30,
    'description': """
Invoicing
====================
Customizations for invoicing.

For now just custom invoice report
    """,
    'category' : 'Sale',
    'author': 'Sneldev <info@sneldev.com>',
    'depends' : ['report', 'account', 'sale'],
    'data': [
        'views/sale_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
