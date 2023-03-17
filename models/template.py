from odoo import models, fields


class ProjectTemplate(models.Model):
    _name = 'project.template'

    name = fields.Char()
    task_name = fields.Char(string="Name of the task")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    user_id = fields.Many2one('res.users', string='Project Manager',
                              default=lambda self: self.env.user, tracking=True)
    tag_ids = fields.Many2many('project.tags', string='Tags')
    description = fields.Html(help="Description")
    project_count = fields.Integer(compute='compute_project_count')

    def create_project(self):
        project_id = self.env['project.project'].create([{
            'name': self.name,
            'label_tasks': self.task_name,
            'tag_ids': self.tag_ids,
            'description': self.description,
            'project_template_id': self.id
        }])
        task_id = self.env['task.template'].search([('project_template_id', '=', self.id)])
        for rec in task_id:
            self.env['project.task'].create([{
                'name': rec.name,
                'project_id': project_id.id,
                'tag_ids': rec.tag_ids,
                'description': rec.description,
                'task_template_id': rec.id
            }])

    def get_project(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Projects',
            'view_mode': 'tree,form',
            'res_model': 'project.project',
            'domain': [('project_template_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def compute_project_count(self):
        for record in self:
            record.project_count = self.env['project.project'].search_count(
                [('project_template_id', '=', self.id)])
