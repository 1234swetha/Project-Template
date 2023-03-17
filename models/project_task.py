from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_template_id = fields.Many2one('task.template', string="Task Template")

    def create_task_template(self):
        if self.project_id.project_template_id.id:
            temp_id = self.env['project.project'].search(
                [('project_template_id', '=', self.project_id.project_template_id.id)])
        else:
            temp_id = self.env['project.template'].create([{
                'name': self.project_id.name,
                'task_name': self.project_id.label_tasks,
                'tag_ids': self.project_id.tag_ids,
                'description': self.project_id.description
            }])

        self.task_template_id = self.env['task.template'].create([{
            'name': self.name,
            'project_template_id': temp_id.id,
            'tag_ids': self.tag_ids,
            'description': self.description,
            'user_ids': self.user_ids
        }])
