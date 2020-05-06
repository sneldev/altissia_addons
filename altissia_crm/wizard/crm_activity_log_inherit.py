# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import timedelta

class CrmActivityLog(models.TransientModel):
    _inherit = 'crm.activity.log'

    date_action = fields.Datetime('Next Activity Time')

    @api.multi
    def action_schedule(self):
        res = super(CrmActivityLog, self).action_schedule()
        for log in self:
            if(log.next_activity_id.name=='Meeting' and log.date_action and log.title_action):
                meeting_values = {
                    'name': log.title_action,
                    'is_activity': True,
                    'duration': 1.0,
                    'opportunity_id': log.lead_id.id,
                    'partner_ids': [(6, 0, [log.lead_id.partner_id.id, self.env.user.partner_id.id])],
                    'user_id': self.env.user.id,
                    'start': log.date_action,
                    'stop': str(fields.Datetime.from_string(log.date_action) + timedelta(hours=1.0)),
                }

                meeting = self.env['calendar.event'].create(meeting_values)
        return res

    @api.multi
    def action_log_and_schedule(self):
        res = super(CrmActivityLog, self).action_log_and_schedule()

        for log in self:
            old_meeting_activity = self.env['calendar.event'].search([('is_activity', '=', True), ('opportunity_id', '=', log.lead_id.id)])

            if ((log.next_activity_id.name == 'Meeting') and log.date_action and log.title_action and (not old_meeting_activity)):
                meeting_values = {
                    'name': log.title_action,
                    'is_activity': True,
                    'duration': 1.0,
                    'opportunity_id': log.lead_id.id,
                    'partner_ids': [(6, 0, [log.lead_id.partner_id.id, self.env.user.partner_id.id])],
                    'user_id': self.env.user.id,
                    'start': log.date_action,
                    'stop': str(fields.Datetime.from_string(log.date_action) + timedelta(hours=1.0)),
                }

                meeting = self.env['calendar.event'].create(meeting_values)
        return res