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
from openerp.fields import Char
from openerp.models import Model, api, _


class CrmLead(Model):
    _inherit = 'crm.lead'

    @api.multi
    def open_form_view(self):
        if self[0].type == 'lead':
            name = _('Leads')
            res = self.env.ref('crm.crm_case_form_view_leads')
        else:
            name = _('Opportunities')
            res = self.env.ref('crm.crm_case_form_view_oppor')
        return {
            'name': name or '',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res.id],
            'res_model': 'crm.lead',
            'context': "{}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'res_id': self[0].id or False
        }


    @api.onchange('partner_id')
    def on_change_partner_id(self):
        result = super(CrmLead, self)._onchange_partner_id_values(self.partner_id.id if self.partner_id else False)
        if not self.partner_id:
            return result


        partner = self.env['res.partner'].browse(self.partner_id.id)
        result.update({'website': partner.website})
        return result



    @api.model
    def _lead_create_contact(self, name, is_company, parent_id=False):
        partner_id = super(CrmLead, self)._lead_create_contact(name, is_company, parent_id)
        self.env['res.partner'].browse(partner_id.id).write({'website': self.website})
        return partner_id


    @api.model
    def create(self, values):
        if values.get('stage_id'):
            crm_stage_rec = self.env['crm.case.stage'].browse(values.get('stage_id'))
            values.update({'probability': crm_stage_rec.probability})
        return super(CrmLead, self).create(values)


    website = Char('Website', size=64, help="Website of Partner or Company")