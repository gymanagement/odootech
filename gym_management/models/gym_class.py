from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GymClass(models.Model):
    _name = 'gym.class'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Gym Group Class'

    name = fields.Char(string='Class Name', required=True)
    trainer_id = fields.Many2one('gym.trainer', string='Trainer', required=True)
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)
    duration = fields.Float(string='Duration (minutes)', compute='_compute_duration', store=True)
    capacity = fields.Integer(string='Capacity', default=15)
    booked_members_ids = fields.Many2many('gym.member', 'gym_class_member_rel', 'class_id', 'member_id', string='Booked Members')
    current_bookings = fields.Integer(string='Current Bookings', compute='_compute_current_bookings', store=True)
    available_slots = fields.Integer(string='Available Slots', compute='_compute_available_slots', store=True)
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ], string='Status', default='draft', tracking=True)

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                delta = rec.end_time - rec.start_time
                rec.duration = delta.total_seconds() / 60.0
            else:
                rec.duration = 0.0

    @api.depends('booked_members_ids')
    def _compute_current_bookings(self):
        for rec in self:
            rec.current_bookings = len(rec.booked_members_ids)

    @api.depends('capacity', 'current_bookings')
    def _compute_available_slots(self):
        for rec in self:
            rec.available_slots = rec.capacity - rec.current_bookings

    @api.constrains('start_time', 'end_time')
    def _check_start_end_time(self):
        for rec in self:
            if rec.start_time and rec.end_time and rec.start_time >= rec.end_time:
                raise ValidationError(_("End time must be after start time."))

    def action_schedule_class(self):
        self.state = 'scheduled'

    def action_cancel_class(self):
        self.state = 'cancelled'

    def action_complete_class(self):
        self.state = 'completed'

    def action_book_class(self):
        # This method would typically be called from the portal or a specific UI action
        # For backend, you might manually add members to booked_members_ids
        self.ensure_one()
        if self.available_slots <= 0:
            raise ValidationError(_("No available slots for this class."))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Book Class'),
            'res_model': 'gym.member',
            'view_mode': 'kanban,list,form',
            'domain': [('subscription_status', '=', 'active')],
            'context': {'default_class_id': self.id}, # Pass class ID to member selection
            'target': 'new', # Open in a dialog/new window
        }

    def action_unbook_class(self):
        # Similar to booking, this would be from portal or specific UI
        self.ensure_one()
        pass

