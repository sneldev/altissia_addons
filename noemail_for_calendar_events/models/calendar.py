# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class Lead(models.Model):
#
#         _inherit = "crm.lead"
#
#         @api.multi
#         def action_schedule_meeting(self):
#             action = super(Lead, self).action_schedule_meeting()
#
#             action['context'].pop('default_partner_ids', False)
#
#             return action
#

class Attendee(models.Model):
    """ Calendar Attendee Information """

    _inherit = 'calendar.attendee'


    @api.multi
    def _send_mail_to_attendees(self, template_xmlid, force_send=False):

        return super(Attendee, self.with_context(no_mail_to_attendees = True))._send_mail_to_attendees(template_xmlid, force_send)