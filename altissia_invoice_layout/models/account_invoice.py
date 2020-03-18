# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    active = fields.Boolean('Active', default=True,
                            help="If the active field is set to False, it will allow you to hide the invoices canceled .")
    delivery_contact_id = fields.Many2one('res.partner', domain=[('is_company','=',False)], string="Delivery contact")
    use_parent_address = fields.Boolean(
        'Use Customer Address for Delivery',
        help="Select this if you want to use customer's address  information as delivery address",
        default=True
    )

    @api.multi
    def write(self, vals):
        for inv in self:
            if(inv and inv.state == 'cancel'):
                if('active' in vals):
                    if( vals.get('active') == False):
                        for inv_line in inv.invoice_line_ids:
                            inv_line.active = False
                    else:
                        inv_lines = self.env['account.invoice.line'].search([('invoice_id', '=', inv.id), ('active', '=', False)])
                        for inv_line in inv_lines:
                            inv_line.active = True
        return super(AccountInvoice, self).write(vals)

    @api.depends('partner_id')
    def _get_company_id(self):
		for record in self:
			record.partner_company = record.partner_id.id if record.partner_id.is_company else record.partner_id.parent_id.id

    partner_company = fields.Many2one('res.partner',string="Customer Company",compute='_get_company_id')

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    active = fields.Boolean('Active', default=True, help="disactivated invoice line if invoice is disactive .")

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

    proj_start_date = fields.Date(string="Start Date")

    @api.model
    def create(self, vals):
        invoice_line = super(AccountInvoiceLine, self).create(vals)
        # if invoice_line.invoice_id.state == 'draft' and not invoice_line.proj_start_date :
        #     raise ValidationError(_('Start Date field must be filled !'))
        return invoice_line
