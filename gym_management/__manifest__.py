{
    'name' : 'Gym Management System',
    'version' : '1.0',
    'summary': 'Gym Management System',
    'sequence': 30,
    'description': """ The first module to learn odoo 18.""",
    'category': 'tool',
    'website': '',
    'depends': ['account','base', 'point_of_sale', 'stock', 'sale_management','hr'],
    'data': [
        # 'security/gym_security.xml',
        'security/ir.model.access.csv',
        'views/sub_management.xml',
        'views/sale_order_line.xml',
        'views/gym_member_views.xml',
        'views/gym_member.xml',
        'views/membership_view.xml',
         'views/workout_plans_view.xml',
        'views/workout_schedule_view.xml',
       

        
    ],
    'application': True,
   
    'license': 'LGPL-3',
}
