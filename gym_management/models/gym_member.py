from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GymMember(models.Model):
    _name = 'gym.member'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin'] # Inherit mail.thread for chatter, mail.activity.mixin for activities, portal.mixin for portal access
    _description = 'Gym Member'

    name = fields.Char(string='Full Name', required=True, tracking=True)
    member_id = fields.Char(string='Member ID', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Phone Number', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    address = fields.Text(string='Address')
    id_upload = fields.Binary(string='ID Document', attachment=True) # For uploading ID
    id_filename = fields.Char(string='ID Filename')
    image_1920 = fields.Image(string="Image", max_width=1920, max_height=1920) # Added image field

    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone')
    emergency_contact_relation = fields.Char(string='Emergency Contact Relation')

    fitness_goals = fields.Text(string='Fitness Goals')
    health_conditions = fields.Text(string='Health Conditions (e.g., allergies, injuries)')
    
    subscription_ids = fields.One2many('gym.subscription', 'member_id', string='Subscriptions')
    active_subscription_id = fields.Many2one('gym.subscription', string='Active Subscription', compute='_compute_active_subscription', store=True)
    subscription_status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled')
    ], string='Subscription Status', compute='_compute_subscription_status', store=True, tracking=True)

    visit_history_ids = fields.One2many('gym.attendance', 'member_id', string='Visit History')
    workout_plan_ids = fields.One2many('gym.workout.plan', 'member_id', string='Workout Plans')
    diet_plan_ids = fields.One2many('gym.diet.plan', 'member_id', string='Diet Plans')
    class_booking_ids = fields.Many2many('gym.class', 'gym_class_member_rel', 'member_id', 'class_id', string='Booked Classes')

    # Computed fields for member progress
    weight = fields.Float(string='Current Weight (kg)', tracking=True)
    bmi = fields.Float(string='BMI', compute='_compute_bmi', store=True, tracking=True)
    height = fields.Float(string='Height (cm)', tracking=True) # Added for BMI calculation

    # Link to Odoo user for portal access
    user_id = fields.Many2one('res.users', string='Portal User', copy=False)

    @api.model
    def create(self, vals):
        if vals.get('member_id', _('New')) == _('New'):
            vals['member_id'] = self.env['ir.sequence'].next_by_code('gym.member.sequence') or _('New')
        member = super(GymMember, self).create(vals)
        return member

    @api.depends('height', 'weight')
    def _compute_bmi(self):
        for member in self:
            if member.weight and member.height:
                member.bmi = member.weight / ((member.height / 100) ** 2)
            else:
                member.bmi = 0.0

    @api.depends('subscription_ids.state', 'subscription_ids.end_date')
    def _compute_active_subscription(self):
        for member in self:
            active_sub = self.env['gym.subscription'].search([
                ('member_id', '=', member.id),
                ('state', '=', 'active'),
                ('end_date', '>=', fields.Date.today())
            ], order='end_date desc', limit=1)
            member.active_subscription_id = active_sub.id if active_sub else False

    @api.depends('active_subscription_id')
    def _compute_subscription_status(self):
        for member in self:
            if member.active_subscription_id and member.active_subscription_id.state == 'active' and member.active_subscription_id.end_date >= fields.Date.today():
                member.subscription_status = 'active'
            elif member.active_subscription_id and member.active_subscription_id.state == 'pending':
                member.subscription_status = 'pending'
            elif member.active_subscription_id and member.active_subscription_id.state == 'cancelled':
                member.subscription_status = 'cancelled'
            else:
                member.subscription_status = 'expired'

    @api.constrains('email')
    def _check_unique_email(self):
        for member in self:
            if member.email and self.search_count([('email', '=', member.email), ('id', '!=', member.id)]) > 0:
                raise ValidationError(_("A member with this email already exists!"))

    def action_view_subscriptions(self):
        self.ensure_one()
        return {
            'name': _('Subscriptions'),
            'type': 'ir.actions.act_window',
            'res_model': 'gym.subscription',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }

    def action_view_workout_plans(self):
        self.ensure_one()
        return {
            'name': _('Workout Plans'),
            'type': 'ir.actions.act_window',
            'res_model': 'gym.workout.plan',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }

    def action_view_diet_plans(self):
        self.ensure_one()
        return {
            'name': _('Diet Plans'),
            'type': 'ir.actions.act_window',
            'res_model': 'gym.diet.plan',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }

    def action_view_attendance(self):
        self.ensure_one()
        return {
            'name': _('Attendance History'),
            'type': 'ir.actions.act_window',
            'res_model': 'gym.attendance',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }

    # Portal related methods
    def action_portal_ensure_user(self): # Renamed from _portal_ensure_user
        """ Create a portal user for the member if one does not exist. """
        self.ensure_one()
        if not self.user_id:
            user = self.env['res.users'].sudo().create({
                'name': self.name,
                'login': self.email or self.member_id,
                'email': self.email,
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])] # Assign to Portal group
            })
            self.user_id = user
        return self.user_id

    def get_portal_url(self):
        self.ensure_one()
        return self.sudo()._get_share_url(redirect=True, signup_token=True)

    def _get_report_base_filename(self):
        self.ensure_one()
        return f'Gym Member - {self.name}'

