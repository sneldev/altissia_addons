# -*- coding: utf-8 -*-
from odoo import fields, api, models, tools, _
from vat_display import vat_display

class Partner(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.depends('vat')
    def _get_vat_display(self):
        self.vat_display = self.vat and vat_display(self.vat)

    @api.one
    @api.depends('name')
    def _get_person_name(self):
        self.person_name = self.name

    person_name = fields.Char(string="Person Name", compute="_get_person_name")
    vat_display = fields.Char(string="Vat Display", compute="_get_vat_display")

    out_inv_comm_type = fields.Selection(default='bba')
    out_inv_comm_algorithm = fields.Selection(default='random')

