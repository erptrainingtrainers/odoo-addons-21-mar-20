#-*- coding:utf-8 -*-
{
    'name': 'College Base',
    'category': 'College Management System',
    'version': '13.0',
    'sequence': 1,
    'author': 'Training',
    'summary': 'Training',
    'description': "Training",
    'depends': ['mail','base'
    ],
    'demo':[],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/staff_views.xml',
        'views/menus.xml',
        'data/data.xml',
    ],
    'qweb':[],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
