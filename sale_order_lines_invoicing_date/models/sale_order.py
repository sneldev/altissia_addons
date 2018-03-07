# -*- coding: utf-8 -*-

from odoo import models, fields
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    next_invoice_date = fields.Date(compute="_get_date_of_next_invoice", string='Date of next invoice', store=False)
    total_invoiced = fields.Float(compute="_get_total_invoiced", string='Total invoiced', digits=dp.get_precision('Account'), store=False)

    def _get_date_of_next_invoice(self):
        for rec in self:
            rec.next_invoice_date = False
            closest_line = self.env['sale.order.line'].search([('order_id','=',rec.id),('invoice_status','!=','invoiced'),('invoice_target_date','!=',False)], limit=1, order='invoice_target_date asc')
            if closest_line:
                rec.next_invoice_date = closest_line[0].invoice_target_date

    def _get_total_invoiced(self):
        for rec in self:
            already_invoiced = self.env['sale.order.line'].search([('order_id','=',rec.id),('invoice_status','=','invoiced')])
            rec.total_invoiced = 0
            for l in already_invoiced:
                rec.total_invoiced += l.price_subtotal
