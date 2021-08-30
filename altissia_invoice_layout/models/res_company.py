# -*- coding: utf-8 -*-
from odoo import fields, api, models, tools, _
from vat_display import vat_display


class Company(models.Model):

    @api.one
    @api.depends('vat')
    def _get_vat_display(self):
        self.vat_display = self.vat and vat_display(self.vat)

    _inherit = 'res.company'
    invoice_footer = fields.Text('Invoice Footer', help="ALtissia Custom Invoice Footer")
    vat_display = fields.Char("Vat Number (display)", compute="_get_vat_display")

    gst_hst = fields.Char("GST/HST - TPS/TVH")
    qst = fields.Char("QST - TVQ")
    
    canadian_specific = fields.Boolean("Canandian Specific", default=False)
    mexicain_specific = fields.Boolean("Mexicain Specific", default=False)
    brazilian_specific = fields.Boolean("Brazilian Specific", default=False)
