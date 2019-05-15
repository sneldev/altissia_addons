# -*- encoding: utf-8 -*-

{
    "name": "CRM Activity Mailing",
    "version": "0.1",
    "category": "CRM",
    "description": """Send mails about crm next activity for users that approve this feature""",
    "depends": ['crm'],
    'data': [
         'data/cron.xml',
         'views/res_users_view.xml',
    ],
    "installable": True,
    "active": True
}
