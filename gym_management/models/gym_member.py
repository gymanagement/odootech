from odoo import models, fields

class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'

    name = fields.Char(string='Full Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    id_number = fields.Char(string='ID Number')
    emergency_contact = fields.Char(string='Emergency Contact')
    subscription_status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending')
    ], string='Subscription Status', default='pending')
    goals = fields.Text(string='Fitness Goals')
