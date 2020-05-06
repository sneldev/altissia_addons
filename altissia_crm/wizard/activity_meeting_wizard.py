# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from datetime import timedelta

class ActivityMeetingWizard(models.TransientModel):
    _name = 'activity.meeting.wizard'

    def transform_old_activity_in_meeting(self):

        meeting_id = self.env['crm.activity'].search([('name', '=', 'Meeting')]).id
        opp_ids = self.env['calendar.event'].search([('is_activity', '=', True)]).mapped('opportunity_id')
        opp_no_act_meeting_ids = self.env['crm.lead'].search([('id', 'not in', opp_ids.ids), ('next_activity_id','=',meeting_id)])
        for opp in opp_no_act_meeting_ids:
            if(opp.date_action):
                meeting_values = {
                    'is_activity': True,
                    'duration': 1.0,
                    'opportunity_id': opp.id,
                    'partner_ids': [(6, 0, [opp.partner_id.id, self.env.user.partner_id.id])],
                    'user_id': self.env.user.id,
                    'start': opp.date_action,
                    'stop': str(fields.Datetime.from_string(opp.date_action) + timedelta(hours=1.0)),
                }

                if opp.title_action:
                    meeting_values['name'] = opp.title_action
                else:
                    meeting_values['name'] = 'Meeting ' + opp.name

                meeting = self.env['calendar.event'].create(meeting_values)

