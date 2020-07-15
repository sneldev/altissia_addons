# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date

class ExpectedClosingYear(models.Model):
    _name = 'expected.closing.year'
    _rec_name = 'year'

    year = fields.Integer('Year', required=True)
    active = fields.Boolean(default=True)

    @api.model
    def action_cron_expected_closing_ancient_year(self):
        '''-- Cron Make old expected closing years inactive --
        '''
        year = date.today().year
        expct_closing_year_active_ids = self.search(
            [('year', '<', year)])

        for year_expect in expct_closing_year_active_ids:
            year_expect.active = False
        return True
