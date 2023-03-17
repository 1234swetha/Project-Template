{
    'name': 'Project Template',
    'version': '16.0.1.0.0',
    'installable': True,
    'application': True,
    'auto_install': False,
    'depends': [
        'project',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/task_template.xml',
        'views/project.xml',
        # 'views/project_wizard.xml',
        'views/project_task.xml',
    ],
}
