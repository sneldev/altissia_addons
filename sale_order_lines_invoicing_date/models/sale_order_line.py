# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields

def get_now(self):
    return datetime.now()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #invoice_status = fields.Selection(INVOICE_STATUSES, string='Invoice status')


    invoice_target_date = fields.Date(string='Invoice Target date')

    date_invoice = fields.Date(string='Date Invoice', compute="_get_date_invoice",store=False)
    def _get_date_invoice(self):
        for rec in self:
            rec.date_invoice = False
            for iline in rec.invoice_lines:
                if iline.invoice_id:
                    rec.date_invoice = iline.invoice_id.date_invoice
                    break
