# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError

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

    journal_refund_id = fields.Many2one('account.journal',string="Refund Journal")

class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    @api.multi
    def compute_refund(self, mode='refund'):
        inv_obj = self.env['account.invoice']
        inv_tax_obj = self.env['account.invoice.tax']
        inv_line_obj = self.env['account.invoice.line']
        context = dict(self._context or {})
        xml_id = False

        for form in self:
            created_inv = []
            date = False
            description = False
            for inv in inv_obj.browse(context.get('active_ids')):
                if inv.state in ['draft', 'proforma2', 'cancel']:
                    raise UserError(_('Cannot refund draft/proforma/cancelled invoice.'))
                if inv.reconciled and mode in ('cancel', 'modify'):
                    raise UserError(_(
                        'Cannot refund invoice which is already reconciled, invoice should be unreconciled first. You can only refund this invoice.'))

                date = form.date or False
                description = form.description or inv.name
                journal = inv.journal_id.id
                if inv.journal_id.journal_refund_id:
                    journal = inv.journal_id.journal_refund_id.id
                refund = inv.refund(form.date_invoice, date, description, journal)
                refund.compute_taxes()

                created_inv.append(refund.id)
                if mode in ('cancel', 'modify'):
                    movelines = inv.move_id.line_ids
                    to_reconcile_ids = {}
                    to_reconcile_lines = self.env['account.move.line']
                    for line in movelines:
                        if line.account_id.id == inv.account_id.id:
                            to_reconcile_lines += line
                            to_reconcile_ids.setdefault(line.account_id.id, []).append(line.id)
                        if line.reconciled:
                            line.remove_move_reconcile()
                    refund.action_invoice_open()
                    for tmpline in refund.move_id.line_ids:
                        if tmpline.account_id.id == inv.account_id.id:
                            to_reconcile_lines += tmpline
                            to_reconcile_lines.reconcile()
                    if mode == 'modify':
                        invoice = inv.read(
                            ['name', 'type', 'number', 'reference',
                             'comment', 'date_due', 'partner_id',
                             'partner_insite', 'partner_contact',
                             'partner_ref', 'payment_term_id', 'account_id',
                             'currency_id', 'invoice_line_ids', 'tax_line_ids',
                             'journal_id', 'date'])
                        invoice = invoice[0]
                        del invoice['id']
                        invoice_lines = inv_line_obj.browse(invoice['invoice_line_ids'])
                        invoice_lines = inv_obj.with_context(mode='modify')._refund_cleanup_lines(invoice_lines)
                        tax_lines = inv_tax_obj.browse(invoice['tax_line_ids'])
                        tax_lines = inv_obj._refund_cleanup_lines(tax_lines)
                        invoice.update({
                            'type': inv.type,
                            'date_invoice': form.date_invoice,
                            'state': 'draft',
                            'number': False,
                            'invoice_line_ids': invoice_lines,
                            'tax_line_ids': tax_lines,
                            'date': date,
                            'origin': inv.origin,
                            'fiscal_position_id': inv.fiscal_position_id.id,
                        })
                        for field in ('partner_id', 'account_id', 'currency_id',
                                      'payment_term_id', 'journal_id'):
                            invoice[field] = invoice[field] and invoice[field][0]
                        inv_refund = inv_obj.create(invoice)
                        if inv_refund.payment_term_id.id:
                            inv_refund._onchange_payment_term_date_invoice()
                        created_inv.append(inv_refund.id)
                xml_id = (inv.type in ['out_refund', 'out_invoice']) and 'action_invoice_tree1' or \
                         (inv.type in ['in_refund', 'in_invoice']) and 'action_invoice_tree2'
                # Put the reason in the chatter
                subject = _("Invoice refund")
                body = description
                refund.message_post(body=body, subject=subject)
        if xml_id:
            result = self.env.ref('account.%s' % (xml_id)).read()[0]
            invoice_domain = safe_eval(result['domain'])
            invoice_domain.append(('id', 'in', created_inv))
            result['domain'] = invoice_domain
            return result
        return True
