# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
import time

import logging
logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"

    task_summary_mail = fields.Boolean('Receive tasks summary email', default=False)

    @api.model
    def crm_activity_mail_send(self):
        # for usr in self.env['res.users'].search([('id','=',131)]):
        print(self.env['res.users'].search([]))
        for usr in self.env['res.users'].search([]):
            if usr.task_summary_mail:
                action_pool = self.env['ir.actions.act_window']
                url = self.env["ir.config_parameter"].get_param("web.base.url")
                print()
                action_id = action_pool.with_context(lang='en_US').search([('res_model', '=', 'crm.lead'),('view_type', '=', 'form'),('name', '=', "Next Activities")], order='id asc')[0]

                record_ids = self.env['crm.lead'].search([('type','=','opportunity'), ('date_action', '!=', False),('user_id','=',usr.id)])
                logger.info(datetime.today().date())
                logger.info(record_ids)
                logger.info(usr.id)
                logger.info("********************************************")
                lst_late = []
                lst_7_future = []
                lst_future = []
                for rec in record_ids:
                    date_action = fields.Date.from_string(rec.date_action)
                    if date.today() > date_action :
                        lst_late.append(rec)
                    if date.today() <= date_action <= date.today() + timedelta(days=7):
                        lst_7_future.append(rec)
                    if date_action > date.today() + timedelta(days=7):
                        lst_future.append(rec)

                body_html=_("""<h2>Today's date - %s - </h2>""" % (datetime.today().date().strftime("%d/%m/%Y")))
                if len(lst_late)>0:
                    body_html += _(""" 
                                    <div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34);">
                                    <br/>
                                    <h1>Late tasks : </h1>
                                    <table style="border-collapse:collapse; border-spacing:0;width:90%">
                                    <tr>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Name</td>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Activity Type</td>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Summary</td>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Activity Link</td>
                                    </tr>
                                """)

                    for record in lst_late:
                        activity_url = url + '/web?#' + 'id=' + str(
                            record.id) + '&view_type=form' + '&model=crm.lead' + '&action=' + str(action_id.id)

                        body_html += _("""<tr>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;">""" + (record.name or ' ') + """</td>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;">""" + (record.next_activity_id.name or ' ') + """</td>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;">""" + (record.title_action or ' ') + """</td>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;"><a href=\"""" + activity_url + """\">Open Activity</a></td>
                                         </tr>""")

                    body_html += """</table><br/><br/>"""

                if len(lst_7_future) > 0:
                    body_html += _(""" 
                                    <div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34);">
                                    <br/>
                                    <h1>Tasks in the next 7 days : </h1>
                                    <table style="border-collapse:collapse; border-spacing:0;width:90%">
                                    <tr>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Name</td>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Activity Type</td>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Summary</td>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Activity Link</td>
                                    </tr>
                                """)

                    for record in lst_7_future:
                        activity_url = url + '/web?#' + 'id=' + str(
                            record.id) + '&view_type=form' + '&model=crm.lead' + '&action=' + str(action_id.id)

                        body_html += _("""<tr>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;">""" + (record.name or ' ') + """</td>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;">""" + (record.next_activity_id.name or ' ') + """</td>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;">""" + (record.title_action or ' ') + """</td>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;"><a href=\"""" + activity_url + """\">Open Activity</a></td>
                                         </tr>""")

                    body_html += """</table><br/><br/>"""

                if len(lst_future) > 0:
                    body_html += _(""" 
                                    <div style="font-family: 'Lucica Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34);">
                                    <br/>
                                    <h1>Future tasks : </h1>
                                    <table style="border-collapse:collapse; border-spacing:0;width:90%">
                                    <tr>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Name</td>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Activity Type</td>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Summary</td>
                                        <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;font-style:italic;background-color:#c0c0c0;vertical-align:top">Activity Link</td>
                                    </tr>
                                """)

                    for record in lst_future:
                        activity_url = url + '/web?#' + 'id=' + str(
                            record.id) + '&view_type=form' + '&model=crm.lead' + '&action=' + str(action_id.id)

                        body_html += _("""<tr>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;">""" + (record.name or ' ') + """</td>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;">""" + (record.next_activity_id.name or ' ') + """</td>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;">""" + (record.title_action or ' ') + """</td>
                                            <td style="font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;"><a href=\"""" + activity_url + """\">Open Activity</a></td>
                                         </tr>""")

                    body_html += """</table><br/><br/>"""
                if record_ids:
                    vals = {
                        # 'subject': _('Your CRM Activities - ' + datetime.today().date().strftime("%d/%m/%Y") + ' -'),
                        'subject': _("Your CRM Activities - %s -") % (datetime.today().date().strftime("%d/%m/%Y")),
                        'body': body_html,
                        'body_html': body_html,
                        'reply_to': self.env.user.email or self.env.user.partner_id.email or '',
                        'email_from': self.env.user.email or self.env.user.partner_id.email or '',
                        'email_to': usr.email or usr.partner_id.email,
                    }
                    mail_id = self.env['mail.mail'].create(vals)
                    mail_id.send()
                    time.sleep(3)




