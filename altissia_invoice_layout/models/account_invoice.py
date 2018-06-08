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
        for line in self.env['account.journal'].search([('type', 'in', ['sale', 'purchase'])]):
            if not line.refund_sequence:
                line.write({'refund_sequence':True})
            if line.refund_sequence and not line.refund_sequence_id:
                vals ={
                    'code':line.code,
                    'name':line.name,
                    'company_id':line.company_id.id,
                }
                line.write({'refund_sequence_id': self.sudo()._create_sequence(vals, refund=True).id})