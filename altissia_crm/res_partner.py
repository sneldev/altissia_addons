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
from datetime import datetime, timedelta
from openerp.fields import Boolean
from openerp.models import Model, api


class ResPartner(Model):
    _inherit = 'res.partner'

    @api.multi
    def get_object_activity(self, object_name, partner_field_name, nb_month=24):
        """
        Returns a dictionary containing the active status of the partner concerning the object
        :param nb_month: number of month the partner activity must be checked
        :returns: a dictionary containing the active status of the partner concerning the object
        """
        res = {}
        obj = self.env[object_name]
        start_date = datetime.now() - timedelta(nb_month*365/12)
        for partner in self:
            res.update({partner.id: False})
            lead_recs = obj.search([(partner_field_name, '=', partner.id),
                                            ('create_date', '>=', datetime.strftime(start_date, "%Y-%m-%d 00:00:00"))])

            ## If a child is active than the parent partner must be active too
            active_child = False
            child_recs = self.search([('parent_id', '=', partner.id)])
            res_children = child_recs.get_object_activity(object_name, partner_field_name)
            for res_child in res_children:
                if res_children.get(res_child, False):
                    active_child = True

            if len(lead_recs) or active_child:
                res.update({partner.id: True})

        return res

    @api.multi
    @api.depends('opportunity_count')
    def _get_activity_status(self):
        """
        Returns a dictionary containing the active status in last 24 month
        """
        lead_res = self.get_object_activity('crm.lead', 'partner_id', 24)

        for partner in self:
            if lead_res.get(partner.id):
                partner.is_active = True
            else:
                partner.is_active = False

    is_active = Boolean('Active during last 2 years', compute=_get_activity_status)