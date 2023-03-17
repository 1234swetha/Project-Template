from odoo import models, fields


class TaskTemplate(models.Model):
    _name = 'task.template'

    name = fields.Char()
    project_template_id = fields.Many2one('project.template', string="Project")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    tag_ids = fields.Many2many('project.tags', string='Tags')
    description = fields.Html(help="Description")
    task_count = fields.Integer(compute='compute_task_count')
    user_ids = fields.Many2many('res.users', string='Assignees', tracking=True)

    def create_task(self):
        temp_id = self.env['project.project'].search([('project_template_id', '=', self.project_template_id.id)])
        if not temp_id:
            temp_id = self.env['project.project'].create([{
                'name': self.project_template_id.name,
                'label_tasks': self.project_template_id.task_name,
                'tag_ids': self.project_template_id.tag_ids,
                'project_template_id': self.project_template_id.id,
                'description': self.project_template_id.description
            }])
        self.env['project.task'].create([{
            'name': self.name,
            'project_id': temp_id.id,
            'tag_ids': self.tag_ids,
            'description': self.description,
            'task_template_id': self.id,
            'user_ids': self.user_ids
        }])

    def get_task(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': [('task_template_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def compute_task_count(self):
        for record in self:
            record.task_count = self.env['project.task'].search_count(
                [('task_template_id', '=', self.id)])
