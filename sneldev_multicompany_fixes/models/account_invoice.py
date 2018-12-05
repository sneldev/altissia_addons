# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright --°[¨¨¨¨ Sneldev ]°--
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
from openerp.models import Model, api
from openerp.api import multi, model

import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(Model):
    _inherit = 'account.invoice'


    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        pre_fiscal_position= None
        if self.fiscal_position_id:
            pre_fiscal_position = self.fiscal_position_id.id
        super(AccountInvoice, self)._onchange_partner_id()
        if not self.fiscal_position_id:
            self.fiscal_position_id = pre_fiscal_position

