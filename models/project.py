from odoo import models, fields


class Project(models.Model):
    _inherit = 'project.project'

    project_template_id = fields.Many2one('project.template', string="Project Template")

    def create_template(self):
        pro_id = self.env['project.template'].create([{
            'name': self.name,
            'task_name': self.label_tasks,
            'tag_ids': self.tag_ids,
            'description': self.description
        }])

        task_id = self.env['project.task'].search([('project_id', '=', self.id)])
        for rec in task_id:
            self.env['task.template'].create([{
                'name': rec.name,
                'tag_ids': rec.tag_ids,
                'description': rec.description,
                'project_template_id': pro_id.id
            }])
