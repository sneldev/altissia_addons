# -*- coding: utf-8 -*-
{
    'name' : 'Altissia Invoice Layout',
    'version' : '1.0',
    'summary': 'Custom invoices',
    'sequence': 30,
    'description': """
Invoicing
====================
Customizations for invoicing.

    """,
    'category' : 'Accounting & Finance',
    'author': 'Sneldev <info@sneldev.com>',
    'depends' : ['report', 'account','l10n_be_invoice_bba'],
    'data': [
        'views/res_company_view.xml',
        'data/custom_paperformat.xml',
        'data/automate_refund_journal.xml',
        'views/report.xml',
        'views/layouts.xml',
        'views/report_invoice.xml',
        'views/account_invoice_view.xml',
        'views/bank.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
