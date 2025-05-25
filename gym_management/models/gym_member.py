from odoo import models, fields, api
from datetime import timedelta, date

class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'

    name = fields.Char(string='Full Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    id_number = fields.Char(string='ID Number')
    emergency_contact = fields.Char(string='Emergency Contact')
    image_1920 = fields.Image("Photo", max_width=1920, max_height=1920)
    subscription_status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending')
    ], string='Subscription Status', default='pending', compute='_compute_subscription_status', store=True)

    goals = fields.Text(string='Fitness Goals')

    registration_date = fields.Date(string='Registration Date', default=fields.Date.today)
    subscription_duration_days = fields.Integer(string='Subscription Duration (Days)')
    subscription_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('other', 'Other'),
    ], string='subscription duration', default='monthly', required=True)

    custom_duration_days = fields.Integer(
        string='another duration',
        help='use only, if anther duration'
    )

    subscription_end_date = fields.Date(
        string='subscription end date',

        compute='_compute_end_date',
        store=True
    )

    @api.depends('registration_date', 'subscription_type', 'custom_duration_days')
    def _compute_end_date(self):
        for rec in self:
            if rec.registration_date:
                if rec.subscription_type == 'monthly':
                    duration = 30
                elif rec.subscription_type == 'quarterly':
                    duration = 90
                elif rec.subscription_type == 'yearly':
                    duration = 365
                elif rec.subscription_type == 'other':
                    duration = rec.custom_duration_days or 0
                else:
                    duration = 0

                rec.subscription_end_date = rec.registration_date + timedelta(days=duration)
            else:
                rec.subscription_end_date = False

    @api.depends('registration_date', 'subscription_end_date')
    def _compute_subscription_status(self):
        today = date.today()
        for rec in self:
            if not rec.registration_date or not rec.subscription_end_date:
                rec.subscription_status = 'pending'
            elif rec.subscription_end_date < today:
                rec.subscription_status = 'expired'
            elif rec.registration_date <= today <= rec.subscription_end_date:
                rec.subscription_status = 'active'
            else:
                rec.subscription_status = 'pending'

    def action_renew_subscription(self):
        for rec in self:
            rec.registration_date = date.today()
