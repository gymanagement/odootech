{
    'name': 'Gym Management System',
    'summary': 'Final project Odoo-based system for managing gym operations',
    'description': """final project based odoo 18""",
    'author': 'Ahmed, Asmaa, Mariam, Qabas',
    'website': 'https://github.com/gymanagement/odootech', 
    'category': 'Fitness',
    'version': '1.0',
    'depends': ['base', 'mail', 'account', 'portal'], 
    'data': [
        'security/ir.model.access.csv',
        'report/gym_reports.xml',                # ← ضع هذا قبل
        'report/gym_report_templates.xml',
        'views/gym_member_views.xml',            # ← هذا بعده
        'views/gym_subscription_views.xml',
        'views/gym_trainer_views.xml',
        'views/gym_plan_views.xml',
        'views/gym_class_views.xml',
        'views/gym_attendance_views.xml',
        'views/gym_menu.xml',
        'data/subscription_plan.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

