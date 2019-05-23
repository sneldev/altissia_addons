# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

import logging
logger = logging.getLogger(__name__)



class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def create(self, vals):
        if self._context.get('email_cc'):
            vals['email_cc'] = self._context.get('email_cc')
        res = super(MailMail, self).create(vals)

        return res
    
    
class MailTemplate(models.Model):
    _inherit = "mail.template"
    
    @api.multi
    def generate_email(self, res_ids, fields=None):
        res = super(MailTemplate, self).generate_email(res_ids, fields)
        # Revert sanitization
        for result, res_id in res.iteritems():
            res[res_id]['body'] = res[res_id]['body_html']
        return res
