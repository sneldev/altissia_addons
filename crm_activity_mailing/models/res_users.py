# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
import time

import logging
logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"

    task_summary_mail = fields.Boolean('Receive tasks summary email', default=True)

    @api.model
    def crm_activity_mail_send(self):
        for usr in self.env['res.users'].search([]):
            if usr.task_summary_mail:
                action_pool = self.env['ir.actions.act_window']
                url = self.env["ir.config_parameter"].get_param("web.base.url")
                action_id = action_pool.with_context(lang='en_US').search([('res_model', '=', 'crm.lead'),('view_type', '=', 'form'),('name', '=', "Next Activities")], order='id asc')[0]
                record_ids = self.env['crm.lead'].search([('type','=','opportunity'), ('date_action', '!=', False),('user_id','=',usr.id)])
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

                body_html= """<link href="https://fonts.googleapis.com/css?family=Poppins|Roboto+Slab&display=swap" rel="stylesheet">
                        <div style="font-family: 'Roboto Slab'; font-size: 12px; color: rgb(34, 34, 34);">
                            <div style="height: 100px; width:250px;">
                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" baseProfile="tiny" id="Calque_1" x="0px" y="0px" viewBox="0 0 164.9 33.8" xml:space="preserve">
                        <g>
                            <g>
                                <polygon fill="#1C305C" points="66.8,22.2 66.8,6.8 63.7,6.8 63.7,24.7 73.1,24.7 73.1,22.2   "></polygon>
                                <polygon fill="#1C305C" points="75,6.8 75,9.4 80,9.4 80,24.7 83.1,24.7 83.1,9.4 88.1,9.4 88.1,6.8   "></polygon>
                                <rect x="92.1" y="6.8" fill="#1C305C" width="3.1" height="17.9"></rect>
                                <path fill="#1C305C" d="M111.8,17c-0.5-0.7-1.2-1.2-1.9-1.6c-0.7-0.3-1.7-0.7-2.8-1c-0.9-0.3-1.7-0.5-2.2-0.8    c-0.5-0.2-0.9-0.5-1.2-0.9c-0.3-0.3-0.4-0.8-0.4-1.3c0-0.7,0.2-1.2,0.7-1.6s1.1-0.6,2-0.6s1.6,0.2,2.1,0.7s0.8,1,1,1.6l0.1,0.3    h3.3l-0.1-0.5c-0.2-1.4-0.8-2.5-1.9-3.4s-2.6-1.3-4.4-1.3c-1.2,0-2.2,0.2-3.1,0.6s-1.6,1-2.1,1.7s-0.7,1.6-0.7,2.6    c0,1.1,0.3,2,0.8,2.7s1.2,1.2,1.9,1.5c0.7,0.3,1.6,0.7,2.8,1c0.9,0.3,1.7,0.5,2.2,0.8c0.5,0.2,0.9,0.5,1.3,0.9    c0.3,0.4,0.5,0.8,0.5,1.4c0,0.7-0.2,1.2-0.7,1.7c-0.5,0.4-1.1,0.7-2,0.7c-0.7,0-1.3-0.1-1.8-0.4c-0.5-0.3-0.9-0.6-1.1-1    c-0.3-0.4-0.4-0.8-0.5-1.2v-0.4h-3.3v0.4c0.1,1,0.4,1.9,1,2.7c0.6,0.8,1.4,1.4,2.3,1.8c1,0.4,2.1,0.7,3.3,0.7    c1.3,0,2.4-0.2,3.2-0.7c0.9-0.5,1.6-1.1,2-1.8c0.4-0.8,0.7-1.6,0.7-2.5C112.6,18.6,112.3,17.6,111.8,17z"></path>
                                <path fill="#1C305C" d="M128.6,17c-0.5-0.7-1.2-1.2-1.9-1.6c-0.7-0.3-1.7-0.7-2.8-1c-0.9-0.3-1.7-0.5-2.2-0.8    c-0.5-0.2-0.9-0.5-1.2-0.9c-0.3-0.3-0.4-0.8-0.4-1.3c0-0.7,0.2-1.2,0.7-1.6c0.5-0.4,1.1-0.6,2-0.6s1.6,0.2,2.1,0.7s0.8,1,1,1.6    l0.1,0.3h3.3l-0.1-0.5c-0.2-1.4-0.8-2.5-1.9-3.4c-1.1-0.9-2.6-1.3-4.4-1.3c-1.2,0-2.2,0.2-3.1,0.6s-1.6,1-2.1,1.7    s-0.7,1.6-0.7,2.6c0,1.1,0.3,2,0.8,2.7s1.2,1.2,1.9,1.5s1.6,0.7,2.8,1c0.9,0.3,1.7,0.5,2.2,0.8c0.5,0.2,0.9,0.5,1.3,0.9    c0.3,0.4,0.5,0.8,0.5,1.4c0,0.7-0.2,1.2-0.7,1.7c-0.5,0.4-1.1,0.7-2,0.7c-0.7,0-1.3-0.1-1.8-0.4c-0.5-0.3-0.9-0.6-1.1-1    c-0.3-0.4-0.4-0.8-0.5-1.2v-0.4h-3.3v0.4c0.1,1,0.4,1.9,1,2.7c0.6,0.8,1.4,1.4,2.3,1.8c1,0.4,2.1,0.7,3.3,0.7    c1.3,0,2.4-0.2,3.2-0.7c0.9-0.5,1.6-1.1,2-1.8c0.4-0.8,0.7-1.6,0.7-2.5C129.4,18.6,129.2,17.6,128.6,17z"></path>
                                <rect x="134.2" y="6.8" fill="#1C305C" width="3.1" height="17.9"></rect>
                                <path fill="#1C305C" d="M154.4,4.1L153,1.2h-0.7l-1.4,2.8l-9.5,20.6h3.6l2.3-5h10.9l2.2,5h3.6L154.4,4.1z M157,17.2h-8.7l4.4-9.6    L157,17.2z"></path>
                                <path fill="#1C305C" d="M50.1,4.1l-1.4-2.8H48l-1.4,2.8l-9.5,20.6h3.6l2.3-5h10.9l2.2,5h3.6L50.1,4.1z M52.7,17.2H44l4.4-9.6    L52.7,17.2z"></path>
                            </g>
                            <g>
                                <path fill="#1C305C" d="M50.4,33.2v0.6h-2.1v-4.2h0.6v3.7L50.4,33.2L50.4,33.2z"></path>
                                <path fill="#1C305C" d="M54.1,33h-1.7l-0.2,0.8h-0.6l1.3-4.2h0.8l1.3,4.3h-0.6L54.1,33z M54,32.3l-0.7-2.2l-0.7,2.2H54z"></path>
                                <path fill="#1C305C" d="M59.7,29.5v4.3h-0.6l-1.9-3.1v3.1h-0.6v-4.2h0.6l1.9,3.1v-3.1L59.7,29.5L59.7,29.5z"></path>
                                <path fill="#1C305C" d="M61.4,31.7L61.4,31.7c0-1.5,0.9-2.2,1.8-2.2c0.7,0,1.4,0.5,1.6,1.2l-0.6,0.1c-0.1-0.4-0.5-0.7-1-0.7    c-0.6,0-1.2,0.4-1.2,1.5v0.1c0,1.1,0.6,1.5,1.2,1.5s1-0.4,1-1.1l0,0h-1.1v-0.6h1.8V32c0,1.1-0.8,1.8-1.7,1.8    C62.3,33.8,61.4,33,61.4,31.7z"></path>
                                <path fill="#1C305C" d="M66.6,32v-2.6h0.6V32c0,0.7,0.4,1.1,0.9,1.1c0.6,0,0.9-0.4,0.9-1.1v-2.6h0.6V32c0,1.1-0.7,1.7-1.6,1.7    C67.2,33.8,66.6,33.2,66.6,32z"></path>
                                <path fill="#1C305C" d="M73.7,33H72l-0.2,0.8h-0.6l1.3-4.2h0.8l1.3,4.3H74L73.7,33z M73.5,32.3l-0.7-2.2l-0.7,2.2H73.5z"></path>
                                <path fill="#1C305C" d="M75.8,31.7L75.8,31.7c0-1.5,0.9-2.2,1.8-2.2c0.7,0,1.4,0.5,1.6,1.2l-0.7,0.1c-0.1-0.4-0.5-0.7-1-0.7    c-0.6,0-1.2,0.4-1.2,1.5v0.1c0,1.1,0.6,1.5,1.2,1.5s1-0.4,1-1.1l0,0h-1.1v-0.6h1.8V32c0,1.1-0.8,1.8-1.7,1.8    C76.6,33.8,75.8,33,75.8,31.7z"></path>
                                <path fill="#1C305C" d="M81.6,30v1.3H83v0.6h-1.4V33h1.9v0.7h-2.6v-4.3h2.6V30H81.6z"></path>
                                <path fill="#1C305C" d="M88.4,30v1.3h1.4v0.6h-1.4V33h1.9v0.7h-2.6v-4.3h2.6V30H88.4z"></path>
                                <path fill="#1C305C" d="M96.1,29.5v4.2h-0.7v-3L94.2,33h-0.4l-1.2-2.2v3H92v-4.2h0.7l1.4,2.5l1.4-2.5H96.1z"></path>
                                <path fill="#1C305C" d="M100.7,31c0,0.9-0.6,1.4-1.4,1.4h-0.7v1.4H98v-4.2c0.4,0,0.8,0,1.3-0.1C99.9,29.5,100.7,29.8,100.7,31z     M99.2,31.8c0.4,0,0.8-0.3,0.8-0.8c0-0.6-0.3-0.9-0.8-0.9c-0.2,0-0.4,0-0.6,0v1.7H99.2z"></path>
                                <path fill="#1C305C" d="M102.1,31.7L102.1,31.7c0-1.5,0.9-2.2,1.8-2.2s1.8,0.7,1.8,2.1v0.1c0,1.4-0.9,2.1-1.8,2.1    C102.9,33.8,102.1,33,102.1,31.7z M104.9,31.7L104.9,31.7c0-1.2-0.6-1.6-1.1-1.6c-0.6,0-1.1,0.4-1.1,1.5v0.1    c0,1.1,0.6,1.5,1.1,1.5C104.4,33.2,104.9,32.8,104.9,31.7z"></path>
                                <path fill="#1C305C" d="M111.8,29.5l-1,4.2h-0.6l-0.9-2.9l-0.9,2.9h-0.6l-1-4.2h0.6l0.7,3.1l0.9-3h0.5l0.9,3l0.7-3.1H111.8z"></path>
                                <path fill="#1C305C" d="M113.8,30v1.3h1.4v0.6h-1.4V33h1.9v0.7h-2.6v-4.3h2.6V30H113.8z"></path>
                                <path fill="#1C305C" d="M119.5,33.8l-0.7-1.3h-0.7v1.3h-0.7v-4.2c0.4,0,0.8,0,1.3-0.1c0.6,0,1.4,0.4,1.4,1.5    c0,0.6-0.3,1.1-0.7,1.3l0.8,1.5H119.5z M118.1,31.8h0.6c0.4,0,0.8-0.3,0.8-0.9c0-0.6-0.3-0.9-0.8-0.9c-0.2,0-0.4,0-0.6,0V31.8z"></path>
                                <path fill="#1C305C" d="M121.7,32.7l0.6-0.2c0,0.3,0.3,0.6,0.7,0.6s0.7-0.3,0.7-0.6c0-0.9-2-0.6-2-1.9c0-0.6,0.6-1.1,1.3-1.1    s1.3,0.5,1.4,1.1l-0.6,0.2c-0.1-0.4-0.4-0.6-0.7-0.6c-0.4,0-0.7,0.3-0.6,0.5c0,0.8,1.9,0.5,1.9,1.9c0,0.7-0.5,1.2-1.3,1.2    C122.3,33.8,121.7,33.2,121.7,32.7z"></path>
                                <path fill="#1C305C" d="M131.4,31c0,0.9-0.6,1.4-1.4,1.4h-0.7v1.4h-0.6v-4.2c0.4,0,0.8,0,1.3-0.1C130.6,29.5,131.4,29.8,131.4,31z     M129.9,31.8c0.4,0,0.8-0.3,0.8-0.8c0-0.6-0.3-0.9-0.8-0.9c-0.2,0-0.4,0-0.6,0v1.7H129.9z"></path>
                                <path fill="#1C305C" d="M133.5,30v1.3h1.4v0.6h-1.4V33h1.9v0.7h-2.6v-4.3h2.6V30H133.5z"></path>
                                <path fill="#1C305C" d="M136.9,31.7L136.9,31.7c0-1.5,0.9-2.2,1.8-2.2c0.9,0,1.8,0.7,1.8,2.1v0.1c0,1.4-0.9,2.1-1.8,2.1    S136.9,33,136.9,31.7z M139.8,31.7L139.8,31.7c0-1.2-0.6-1.6-1.1-1.6c-0.6,0-1.1,0.4-1.1,1.5v0.1c0,1.1,0.6,1.5,1.1,1.5    C139.3,33.2,139.8,32.8,139.8,31.7z"></path>
                                <path fill="#1C305C" d="M144.9,31c0,0.9-0.6,1.4-1.4,1.4h-0.7v1.4h-0.6v-4.2c0.4,0,0.8,0,1.3-0.1C144.1,29.5,144.9,29.8,144.9,31z     M143.4,31.8c0.4,0,0.8-0.3,0.8-0.8c0-0.6-0.3-0.9-0.8-0.9c-0.2,0-0.4,0-0.6,0v1.7H143.4z"></path>
                                <path fill="#1C305C" d="M148.5,33.2v0.6h-2.1v-4.2h0.6v3.7L148.5,33.2L148.5,33.2z"></path>
                                <path fill="#1C305C" d="M150.7,30v1.3h1.4v0.6h-1.4V33h1.9v0.7H150v-4.3h2.6V30H150.7z"></path>
                            </g>
                        </g>
                        <g>
                            <path fill="#C2D500" d="M4.6,16c1.2-1.8,2.1-2.3,5.1-2.4c0.1,0,0.3,0,0.4,0v-1.8H7.6c-0.4,0-0.5-0.3-0.5-0.4s0.1-0.3,0.2-0.5   C9.1,7.8,11,4.3,11,4.3c0.1-0.2,0.5-0.3,0.6,0c0.1,0.2,0.1,0.9,0.1,0.9v12.4h4V1.2h-5.2L1.2,17.5h2.5C4,17,4.6,16,4.6,16z"></path>
                            <path fill="#C2D500" d="M1,24.2l16.6,9.2V31c-0.6-0.3-1.4-0.8-1.5-0.9c-1.9-1.2-2.4-2.1-2.5-5c0-0.1,0-0.2,0-0.4h-1.8V27   c0,0.4-0.3,0.5-0.5,0.4c-0.1,0-0.3-0.1-0.5-0.2C7.6,25.5,4,23.6,4,23.6c-0.2-0.1-0.3-0.5,0-0.6C4.2,23,4.9,23,4.9,23h12.7v-3.8H1   V24.2z"></path>
                            <path fill="#C2D500" d="M17.6,1.4v2.4c0.6,0.3,1.5,0.9,1.5,0.9c1.9,1.2,2.4,2.1,2.5,5c0,0.1,0,0.2,0,0.4h1.8V7.9   c0-0.4,0.3-0.5,0.5-0.4c0.1,0,0.3,0.1,0.5,0.2c3.2,1.7,6.8,3.6,6.8,3.6c0.2,0.1,0.3,0.5,0,0.6C31,12,30.3,12,30.3,12H17.6v3.8h16.7   v-5L17.6,1.4z"></path>
                            <path fill="#C2D500" d="M30.6,19c-1.2,1.8-2.1,2.3-5.1,2.4c-0.1,0-0.2,0-0.4,0v1.8h2.4c0.4,0,0.5,0.3,0.5,0.4   c0,0.1-0.1,0.3-0.2,0.5c-1.8,3.1-3.7,6.6-3.8,6.6c-0.1,0.2-0.5,0.3-0.6,0c-0.1-0.2-0.1-0.9-0.1-0.9V17.5h-4v16.2h5.2L34,17.5h-2.5   C31.2,18,30.6,18.9,30.6,19z"></path>
                        </g>
                                </svg>
                            </div>
                        <br/>"""
                if len(lst_late)>0:
                    str_src = _(""" 
                                    <div style="font-family: Poppins; font-size: 20px; font-weight: 700;color: #3d5285;">Late tasks</div>
                                    <table style="border-collapse:collapse; border-spacing:0;width:90%">
                                    <tr>	
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Lead</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Date</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Activity Type</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Summary</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Link</td>
                                    </tr>
                                """)
                    if self.env['ir.translation'].search([('source','=',str_src),('lang','=',usr.lang),('state','=','translated')]):
                        translation = self.env['ir.translation'].search([('source','=',str_src),('lang','=',usr.lang),('state','=','translated')])[-1].value
                    else:
                        translation = str_src
                    body_html += translation

                    for record in lst_late:
                        activity_url = url + '/web?#' + 'id=' + str(
                            record.id) + '&view_type=form' + '&model=crm.lead' + '&action=' + str(action_id.id)

                        body_html += """<tr>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.name or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.date_action or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.next_activity_id.name or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.title_action or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;"><a href=\"""" + activity_url + """\">"""
                        str_src = _("Open Activity")
                        if self.env['ir.translation'].search(
                                [('source', '=', str_src), ('lang', '=', usr.lang), ('state', '=', 'translated')]):
                            translation = self.env['ir.translation'].search(
                                [('source', '=', str_src), ('lang', '=', usr.lang), ('state', '=', 'translated')])[
                                -1].value
                        else:
                            translation = str_src
                        body_html += translation + """</a></td></tr>"""

                    body_html += """</table><br/>"""

                if len(lst_7_future) > 0:
                    str_src = _(""" 
                                    <div style="font-family: Poppins; font-size: 20px; font-weight: 700;color: #3d5285;">Tasks in the next 7 days</div>
                                    <table style="border-collapse:collapse; border-spacing:0;width:90%">
                                    <tr>	
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Lead</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Date</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Activity Type</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Summary</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Link</td>
                                    </tr>
                                """)
                    if self.env['ir.translation'].search([('source','=',str_src),('lang','=',usr.lang),('state','=','translated')]):
                        translation = self.env['ir.translation'].search([('source','=',str_src),('lang','=',usr.lang),('state','=','translated')])[-1].value
                    else:
                        translation = str_src
                    body_html += translation

                    for record in lst_7_future:
                        activity_url = url + '/web?#' + 'id=' + str(
                            record.id) + '&view_type=form' + '&model=crm.lead' + '&action=' + str(action_id.id)

                        body_html += """<tr>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.name or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.date_action or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.next_activity_id.name or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.title_action or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;"><a href=\"""" + activity_url + """\">"""
                        str_src = _("Open Activity")
                        if self.env['ir.translation'].search(
                                [('source', '=', str_src), ('lang', '=', usr.lang), ('state', '=', 'translated')]):
                            translation = self.env['ir.translation'].search(
                                [('source', '=', str_src), ('lang', '=', usr.lang), ('state', '=', 'translated')])[
                                -1].value
                        else:
                            translation = str_src
                        body_html += translation + """</a></td></tr>"""

                    body_html += """</table><br/>"""

                if len(lst_future) > 0:
                    str_src = _(""" 
                                    <div style="font-family: Poppins; font-size: 20px; font-weight: 700;color: #3d5285;">Future tasks</div>
                                    <table style="border-collapse:collapse; border-spacing:0;width:90%">
                                    <tr>	
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Lead</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Date</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Activity Type</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Summary</td>
                                        <td style="padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;font-weight:bold;background-color:#f0f0f0;vertical-align:top">Link</td>
                                    </tr>
                                """)
                    if self.env['ir.translation'].search([('source','=',str_src),('lang','=',usr.lang),('state','=','translated')]):
                        translation = self.env['ir.translation'].search([('source','=',str_src),('lang','=',usr.lang),('state','=','translated')])[-1].value
                    else:
                        translation = str_src
                    body_html += translation

                    for record in lst_future:
                        activity_url = url + '/web?#' + 'id=' + str(
                            record.id) + '&view_type=form' + '&model=crm.lead' + '&action=' + str(action_id.id)

                        body_html += """<tr>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.name or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.date_action or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.next_activity_id.name or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;">""" + (record.title_action or ' ') + """</td>
                                            <td style="font-size:14px;padding:5px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;color:#9091af;"><a href=\"""" + activity_url + """\">"""
                        str_src = _("Open Activity")
                        if self.env['ir.translation'].search(
                                [('source', '=', str_src), ('lang', '=', usr.lang), ('state', '=', 'translated')]):
                            translation = self.env['ir.translation'].search(
                                [('source', '=', str_src), ('lang', '=', usr.lang), ('state', '=', 'translated')])[
                                -1].value
                        else:
                            translation = str_src
                        body_html += translation + """</a></td></tr>"""

                    body_html += """</table><br/>"""
                if record_ids:
                    str_src = _("Your CRM Activities - %s")
                    if self.env['ir.translation'].search(
                            [('source', '=', str_src), ('lang', '=', usr.lang), ('state', '=', 'translated')]):
                        translation = self.env['ir.translation'].search(
                            [('source', '=', str_src), ('lang', '=', usr.lang), ('state', '=', 'translated')])[
                            -1].value
                    else:
                        translation = str_src
                    vals = {
                        'subject': (translation) % (datetime.today().date().strftime("%d/%m/%Y")),
                        'body': body_html,
                        'body_html': body_html,
                        'reply_to': self.env.user.email or self.env.user.partner_id.email or '',
                        'email_from': self.env.user.email or self.env.user.partner_id.email or '',
                        'email_to': usr.email or usr.partner_id.email,
                    }
                    mail_id = self.env['mail.mail'].create(vals)
                    mail_id.send()
                    time.sleep(3)




