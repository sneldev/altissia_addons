# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) Sneldev
#    All Rights Reserved.
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
    'name': 'Product Default Service',
    'version': '1.0',
    'author': "Sneldev",
    'website': 'http://www.sneldev.com',
    'license': 'AGPL-3',
    'category': 'Generic Modules',
    'depends': [
        'product'
    ],
    'data': [
    ],
    'demo': [
    ],
    #what's this ??? Seems very cool.
    #'pre_init_hook': 'update_current_products',
    'auto_install': False,
    'installable': True,
}
