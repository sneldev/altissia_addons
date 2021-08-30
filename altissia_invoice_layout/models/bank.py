# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    footer = fields.Boolean("Display on Reports",
                         help="Display this bank account on the footer of printed documents like invoices and sales orders.")
    clabe = fields.Char("Clabe",
                         help="Standardized bank key number")
    bank_id = fields.Many2one('res.bank')


