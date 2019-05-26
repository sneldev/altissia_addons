# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

import logging
logger = logging.getLogger(__name__)

class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    email_cc = fields.Char('Cc')


    @api.multi
    def send_mail(self, auto_commit=False):
        return super(MailComposer, self.with_context({'email_cc':self.email_cc})).send_mail(auto_commit=auto_commit)