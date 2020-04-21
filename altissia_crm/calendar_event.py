# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CalendarEvent(models.Model):

    _inherit = 'calendar.event'

    is_activity = fields.Boolean('Is Activity')