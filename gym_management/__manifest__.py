{
    'name': 'Gym Management System',
    'version': '1.0',
    'summary': 'Manage gym members and operations',
    'description': 'A gym member management system built on Odoo 18',
    'category': 'Fitness & Wellness',  
    'author': 'Ahmed, Asmaa, Mariam, Qabas',
    'depends': ['base'],
    'data': [
        'security/gym_security.xml',
        'security/ir.model.access.csv',
        'views/gym_member_views.xml',
    ],
    'images': ['static/description/gym.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}


