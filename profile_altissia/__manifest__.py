# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright Eezee-it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Profile Altissia",
    "version": "0.1",
    "author": "Eezee-it",
    "category": "CRM",
    "website": "http://www.eezee-it.com",
    "description": """Provide a profile for Altissia
    This module install the module\"Altissia Customization on CRM module\"""",
    "depends": ['altissia_crm', 'altissia_project', 'mass_editing',],
    'data': [
        'data/mass_editing_group.xml',
        'views/mass_editing_view.xml',
    ],
    "installable": True,
    "active": True
}
