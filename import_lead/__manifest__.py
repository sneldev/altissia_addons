# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Import Lead from Excel or CSV File',
    'version': '1.1',
    "price": 15,
    "currency": 'EUR',
    'summary': 'Easy to Import multiple leads data on Odoo by Using CSV/XLS file',
    'description': """Imports Lead From CSV or XLS
        BrowseInfo developed a new odoo/OpenERP module apps.
	    This module use for import bulk leads from Excel file. Import lead from CSV or Excel file.
	Import Lead data,Add lead from excel. Import excel file
""",
    'author': 'BrowseInfo',
    'website': 'http://www.browseinfo.in',
    
    'depends': ['base','sale','crm'],
    'data': [
    		  'import_lead_view.xml',
            ],
    'demo': [],
    'test': [],
    'installable':True,
    'auto_install':False,
    'application':True,
    "live_test_url":'https://youtu.be/nCR38U34XVY',
    "images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
