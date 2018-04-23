# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright Eezee-it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.models import Model
from openerp.api import multi, model
import logging

_logger = logging.getLogger(__name__)


class ProjectTask(Model):
    _inherit = 'project.task'

    @multi
    def write(self, values):
        if 'stage_id' in values:
            stage_id = self.env['project.task.type'].browse(
                [values['stage_id']])
            if str(stage_id.name).lower() == 'done':
                values.update({'remaining_hours': 0.0})
        return super(ProjectTask, self).write(values)

    @model
    def action_cron_task_done(self):
        '''-- Cron reset remaining_hours --
        Reset the remaining hours to 0.0 if the task is 'Done'
        '''
        project_task_type_id = self.env['project.task.type'].search([
            ('name', '=', 'Done')])
        task_ids = self.search([
            ('stage_id', '=', project_task_type_id.id),
            ('remaining_hours', '!=', 0.0)])
        _logger.debug(
            'There are %d tasks to be reset the remaining hours' % len(task_ids))
        if len(task_ids):
            for task in task_ids:
                task.write({'remaining_hours': 0.0})
        return True


'''
UPDATE project_task SET remaining_hours = 0.00
FROM project_task_type
WHERE project_task.stage_id = project_task_type.id
AND project_task_type.name = 'Done' AND project_task.remaining_hours != 0.00
'''
