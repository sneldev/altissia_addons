# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    delivery_contact_id = fields.Many2one('res.partner', domain=[('is_company','=',False)], string="Delivery contact")
    use_parent_address = fields.Boolean(
        'Use Customer Address for Delivery',
        help="Select this if you want to use customer's address  information as delivery address",
        default=True
    )

    @api.depends('partner_id')
    def _get_company_id(self):
		for record in self:
			record.partner_company = record.partner_id.id if record.partner_id.is_company else record.partner_id.parent_id.id

    partner_company = fields.Many2one('res.partner',string="Customer Company",compute='_get_company_id')


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def run_scheduler_refund_journal(self):
        # for rec in self :
        ctx = self.env.context.copy()
        ctx['is_sale_purchase'] = True
        for line in self.env['account.journal'].search([('type', 'in', ['sale', 'purchase'])]):
            if line.sequence_id:
                code = line.sequence_id.prefix[:(line.sequence_id.prefix).find('/')]
            else:
                code = line.code
            if line.refund_sequence_id:
                prefix = self.with_context(ctx)._get_sequence_prefix(code, refund=True)
                line.refund_sequence_id.prefix = prefix
            else:
                vals = {
                    'code': code,
                    'name': line.name + '  Refund',
                    'company_id': line.company_id.id,
                }
                line.write({'refund_sequence_id': self.sudo().with_context(ctx)._create_sequence(vals, refund=True).id})

            line.write({'refund_sequence': True})

    @api.model
    def _get_sequence_prefix(self, code, refund=False):
        ctx = self.env.context
        if ctx.get('is_sale_purchase', False):
            prefix = code.upper()
            if refund:
                prefix = prefix + 'CN'
            return prefix + '/%(range_year)s/'
        else:
            return super(AccountJournal, self)._get_sequence_prefix(code,refund)



class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    proj_start_date = fields.Date(string="Project start date")
