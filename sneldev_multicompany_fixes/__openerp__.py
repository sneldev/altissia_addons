# -*- coding: utf-8 -*-
{
    'name' : 'Sneldev MultiCompany Fixes',
    'version' : '1.0',
    'summary': 'Odoo BugFixes for multicompany',
    'sequence': 30,
    'description': """
Multicompany
====================
Solving problems related to the "defaults" of a user having access to multiple companies
and trying to use company2 objects while its default company is company1
    """,
    'category' : 'Odoo BugFixes',
    'author': 'Sneldev <info@sneldev.com>',
    'depends' : ['account'],
    'data': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

