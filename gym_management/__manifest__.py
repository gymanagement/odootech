{
    "name": "Gym Management System",
    "version": "1.0",
    "summary": "Manage gym members and related operations",
    "description": "A gym member management module for Odoo 18",
    "category": "Fitness",
    "author": "Ahmed, Asmaa, Mariam, Qabas",
    "depends": ["base"],
    "data": [
        "security/gym_security.xml",
        "security/ir.model.access.csv",
        "views/gym_member_views.xml"
    ],
    "installable": True,
    "application": True
}
