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
from openerp.fields import Boolean
from openerp.models import Model, TransientModel, api, _
from openerp import fields
from datetime import datetime, date, timedelta, time

class CrmLead(Model):
    _inherit = 'crm.lead'

    @api.multi
    def get_mail_compose_message(self):
        last_7_days_lead = []
        last_7_days_meeting_new_opp = []
        last_7_days_meeting_not_new_opp = []
        last_7_days_meeting = []
        last_7_days_prop_lead = []
        last_7_days_invoices = []
        next_7_days_meeting = []
        next_7_days_tasks = []
        stage_new_id = self.env.ref('crm.stage_lead1').id
        stage_prop_id = self.env.ref('crm.stage_lead3').id
        meeting_with_new_opp_ids = self.env['crm.lead'].search([('stage_id', '=', stage_new_id), ('type', '=', 'opportunity')]).ids
        meeting_with_not_new_opp_ids = self.env['crm.lead'].search([('stage_id', '!=', stage_new_id), ('type', '=', 'opportunity')]).ids
        meeting_with_opp_ids = self.env['crm.lead'].search([('type', '=', 'opportunity')]).ids

        # 1. NEW LEADS (#)
        for lead in self.env['crm.lead'].search([('user_id','=', self.env.uid), ('type', '=', 'lead')]):
            create_date = fields.Date.from_string(lead.create_date)
            if date.today() + timedelta(days=-7) <= create_date < date.today():
                lead_create_date = create_date.strftime('%d/%m/%y')
                last_7_days_lead.append((lead_create_date or ' _ ', lead.partner_id.name or ' _ ', lead.name or ' _ '))
        count_last_7_days_lead = len(last_7_days_lead)

        # 2.MEETINGS OBTAINED(#) ==> With new opportunities (#)
        for meeting in self.env['calendar.event'].search(
                [('user_id', '=', self.env.uid), ('opportunity_id', 'in', meeting_with_new_opp_ids)]):
            meeting_date = fields.Date.from_string(meeting.start)
            if date.today() + timedelta(days=-7) <= meeting_date < date.today():
                lead_meeting_date = meeting_date.strftime('%d/%m/%y')
                last_7_days_meeting_new_opp.append((lead_meeting_date or ' _ ', meeting.opportunity_id.name or ' _ '))
        count_last_7_days_meeting_new_opp = len(last_7_days_meeting_new_opp)

        # 2.MEETINGS OBTAINED(#) ==> With existing opportunities (#)
        for meeting in self.env['calendar.event'].search([('user_id', '=', self.env.uid), ('opportunity_id', 'in', meeting_with_not_new_opp_ids)]):
            meeting_date = fields.Date.from_string(meeting.start)
            if date.today() + timedelta(days=-7) <= meeting_date < date.today():
                lead_meeting_date = meeting_date.strftime('%d/%m/%y')
                last_7_days_meeting_not_new_opp.append((lead_meeting_date or ' _ ', meeting.opportunity_id.name or ' _ '))
        count_last_7_days_meeting_not_new_opp = len(last_7_days_meeting_not_new_opp)

        count_last_7_days_meeting_opps = count_last_7_days_meeting_new_opp + count_last_7_days_meeting_not_new_opp

        # 3. MEETINGS ATTENDED( # )
        for meeting in self.env['calendar.event'].search([('user_id', '=', self.env.uid), ('opportunity_id','in',meeting_with_opp_ids)]):
            meeting_date = fields.Date.from_string(meeting.start)
            if date.today() + timedelta(days=-7) <= meeting_date < date.today():
                lead_meeting_date = meeting_date.strftime('%d/%m/%y')
                last_7_days_meeting.append((lead_meeting_date or ' _ ', meeting.opportunity_id.name or ' _ ', meeting.name or ' _ '))
        count_last_7_days_meeting = len(last_7_days_meeting)

        # 4. PROPOSALS SENT( # )
        for lead in self.env['crm.lead'].search([('user_id', '=', self.env.uid), ('stage_id', '=', stage_prop_id), ('planned_revenue', '!=', 0), ('type', '=', 'opportunity')]):
            create_date = fields.Date.from_string(lead.create_date)
            if date.today() + timedelta(days=-7) <= create_date < date.today():
                lead_create_date = create_date.strftime('%d/%m/%y')
                last_7_days_prop_lead.append((lead_create_date or ' _ ', lead.name or ' _ ', lead.planned_revenue or ' _ ', lead.company_currency.symbol or ' _ '))
        count_last_7_days_prop_lead = len(last_7_days_prop_lead)

        # 5. INVOICES( # )
        for inv in self.env['account.invoice'].search([('create_uid','=',self.env.uid)]):
            create_date = fields.Date.from_string(inv.create_date)
            if date.today() + timedelta(days=-7) <= create_date < date.today():
                inv_create_date = create_date.strftime('%d/%m/%y')
                last_7_days_invoices.append((inv_create_date or ' _ ', inv.partner_id.name or ' _ ', inv.amount_untaxed_signed or ' _ ', inv.currency_id.symbol or ' _ '))
        count_last_7_days_invoices = len(last_7_days_invoices)

        # Coming week
        # 1. MEETINGS PLANNED( # )
        for meeting in self.env['calendar.event'].search([('user_id', '=', self.env.uid), ('type', '=', 'opportunity')]):
            meeting_date = fields.Date.from_string(meeting.start)
            if date.today() <= meeting_date <= date.today() + timedelta(days=7):
                lead_meeting_date = meeting_date.strftime('%d/%m/%y')
                next_7_days_meeting.append(
                    (lead_meeting_date or ' _ ', meeting.opportunity_id.name or ' _ ', meeting.name or ' _ '))
        count_next_7_days_meeting = len(next_7_days_meeting)

        # 2. TASKS PLANNED( # )
        for task in self.env['crm.lead'].search([('type', '=', 'opportunity'), ('date_action', '!=', False), ('user_id','=', self.env.uid)]):
            date_action = fields.Date.from_string(task.date_action)
            if date.today() <= date_action <= date.today() + timedelta(days=7):
                task_date_action = date_action.strftime('%d/%m/%y')
                next_7_days_tasks.append((task_date_action or ' _ ', task.name or ' _ ', task.planned_revenue or ' _ ', task.company_currency.symbol or ' _ ',  task.title_action or ' _ '))
        count_next_7_days_tasks = len(next_7_days_tasks)

        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('altissia_crm', 'mail_template_crm_sale_report_mail')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'crm.lead',
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'subject':self.env.user.name +_(' Sales Report ')+ datetime.today().date().strftime("%d/%m/%Y"),
            'sale_team': self.env.user.sale_team_id.name,
            'last_7_days_lead': last_7_days_lead,
            'count_last_7_days_lead': count_last_7_days_lead,
            'last_7_days_meeting': last_7_days_meeting,
            'count_last_7_days_meeting': count_last_7_days_meeting,
            'last_7_days_meeting_new_opp': last_7_days_meeting_new_opp,
            'count_last_7_days_meeting_new_opp': count_last_7_days_meeting_new_opp,
            'last_7_days_meeting_not_new_opp': last_7_days_meeting_not_new_opp,
            'count_last_7_days_meeting_not_new_opp': count_last_7_days_meeting_not_new_opp,
            'count_last_7_days_meeting_opps': count_last_7_days_meeting_opps,
            'last_7_days_prop_lead': last_7_days_prop_lead,
            'count_last_7_days_prop_lead': count_last_7_days_prop_lead,
            'last_7_days_invoices': last_7_days_invoices,
            'count_last_7_days_invoices': count_last_7_days_invoices,
            'next_7_days_meeting': next_7_days_meeting,
            'count_next_7_days_meeting': count_next_7_days_meeting,
            'next_7_days_tasks': next_7_days_tasks,
            'count_next_7_days_tasks': count_next_7_days_tasks,
            'email_to': 'projects@altissia.org',
            'default_email_cc': 'nlboel@altissia.org, cbounameaux@altissia.org, tmoreau@altissia.org',
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def compute_lost_visible(self):
        for rec in self:
            if rec.stage_id.name == 'Lost':
                rec.lost_visible = True

    @api.multi
    def action_set_lost(self):
        """ Lost semantic: probability = 0, active = False """
        lost_stage = self.env['crm.stage'].search([('name','=','Lost')])[0]
        return self.write({'probability': 0,'stage_id':lost_stage.id})

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
        # if values.get('stage_id'):
        #     crm_stage_rec = self.env['crm.case.stage'].browse(values.get('stage_id'))
        #     values.update({'probability': crm_stage_rec.probability})
        return super(CrmLead, self).create(values)


    website = Char('Website', size=64, help="Website of Partner or Company")
    lost_visible = Boolean(default=False ,compute='compute_lost_visible',store=False)
   
