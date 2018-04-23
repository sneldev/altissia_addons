# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    footer = fields.Boolean("Display on Reports",
                         help="Display this bank account on the footer of printed documents like invoices and sales orders.")


