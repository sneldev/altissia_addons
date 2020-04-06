# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning
import tempfile
import binascii

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')

from datetime import datetime, timedelta

class import_lead_wizard(models.TransientModel):

    _name = 'import.lead.wizard'

    lead_file = fields.Binary(string="Select File")
    select_option = fields.Selection([('csv', 'CSV'), ('xls', 'XLS')], string="Select File Format")

    @api.multi
    def import_file(self):
        if self.select_option == 'csv':

            keys = ['date', 'customer', 'contact_name' , 'lead', 'function', 'street', 'street_2', 'city', 'state', 'zip', 'country', 'email','phone','sales team' ,'description' ]
            csv_data = base64.b64decode(self.lead_file)
            data_file = cStringIO.StringIO(csv_data)
            data_file.seek(0)
            file_reader = []
            csv_reader = csv.reader(data_file, delimiter=',')
            try:
                file_reader.extend(csv_reader)
            except Exception:
                raise Warning(_("Invalid file!"))
            values = {}
            for i in range(len(file_reader)):
                field = map(str, file_reader[i])
                values = dict(zip(keys, field))
                print("----values",values)
                if values:
                    if i == 0:
                        continue
                    res = self.create_lead(values)
                    
        else:
            fp = tempfile.NamedTemporaryFile(delete= False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.lead_file))
            fp.seek(0)

            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            product_obj = self.env['product.product']
            for row_no in range(sheet.nrows):
                val = {}
                if row_no <= 0:
                    fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    line = (map(lambda row:isinstance(row.value, unicode) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    values.update({


                                    'date' : line[0],
                                    'customer':line[1],
                                    'contact_name' : line[2],
                                    'lead':line[3],
                                    'function' : line[4],
                                   
                                   'street':line[5],
                                   'street_2':line[6],
                                   'city':line[7],
                                   'state':line[8],
                                   'zip':line[9],
                                   'country':line[10],
                                   'email':line[11],
                                   'phone':line[12],
                                   'sales team':line[13],
                                   'description':line[14],




                                })
                    res = self.create_lead(values)
            return res

    @api.multi
    def create_lead(self, values):
        partner_id = self.find_partner(values.get('customer'))
        team_id = self.find_team(values.get('sales team'))
        country = self.find_country(values.get('country'))
        state = self.find_state(values.get('state'),country)
        DATETIME_FORMAT ='%m/%d/%Y %H:%M:%S'
        i_date = datetime.strptime(values.get('date'), DATETIME_FORMAT)   
        str = 'insert into crm_lead (active,name,partner_id,street,zip,city,country_id,phone,email_from,description,team_id,function,street2,state_id,create_date,contact_name,type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self._cr.execute(str, (
            True,
            values.get('lead'),
            partner_id.id,
            values.get('street'),
            values.get('zip'),
            values.get('city'),
            country.id,
            values.get('phone'),
            
            values.get('email'),
            values.get('description'),
            team_id.id,
            
            values.get('function'),
            values.get('street_2'),
            state.id,
            i_date,
            values.get('contact_name'),
            'lead'
            
            ))
    
    @api.multi
    def find_team(self, team):
        team_obj_search = self.env['crm.team'].search([('name', '=', team)])
        if team_obj_search:
            return team_obj_search
        else:
            raise Warning(_('Sales Team "%s" is Not Available') % team)

    @api.multi    
    def find_partner(self, partner):
        partner_obj_search = self.env['res.partner'].search([('name', '=', partner)])
        if partner_obj_search:
            return partner_obj_search
        else:
            partner_id = self.env['res.partner'].create({'name':partner})
            return partner_id


    @api.multi
    def find_country(self, country):
        country_search = self.env['res.country'].search([('name', '=', country)])
        if country_search:
            return country_search
        else:
            raise Warning(_('Country "%s" is Not Available') % country)



    @api.multi
    def find_state(self, state, country ):
        state_search = self.env['res.country.state'].search([('name', '=', state),('country_id','=',country.id)])
        if state_search:
            return state_search

        else :
            state_search = self.env['res.country.state'].search([('code', '=', state),('country_id','=',country.id)])
            if state_search:
                return state_search


        if not state_search :
            raise Warning(_('State "%s" is Not Available') % state)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
