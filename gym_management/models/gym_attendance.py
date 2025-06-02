from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GymAttendance(models.Model):
    _name = 'gym.attendance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Gym Attendance Log'
    _order = 'attendance_date desc, check_in_time desc'

    name = fields.Char(string='Attendance Record', compute='_compute_name', store=True)
    member_id = fields.Many2one('gym.member', string='Member', ondelete='cascade', tracking=True)
    trainer_id = fields.Many2one('gym.trainer', string='Trainer', tracking=True)
    class_id = fields.Many2one('gym.class', string='Class Attended', tracking=True)
    attendance_date = fields.Date(string='Date', default=fields.Date.today(), required=True, tracking=True)
    check_in_time = fields.Datetime(string='Check-in Time', default=fields.Datetime.now(), required=True, tracking=True)
    check_out_time = fields.Datetime(string='Check-out Time', tracking=True)
    duration = fields.Float(string='Duration (hours)', compute='_compute_duration', store=True)
    attendance_type = fields.Selection([
        ('gym_visit', 'Gym Visit'),
        ('class_attendance', 'Class Attendance')
    ], string='Attendance Type', default='gym_visit', required=True, tracking=True)
    notes = fields.Text(string='Notes')

    @api.depends('member_id', 'attendance_date', 'check_in_time')
    def _compute_name(self):
        for rec in self:
            member_name = rec.member_id.name if rec.member_id else "N/A"
            date_str = fields.Date.to_string(rec.attendance_date) if rec.attendance_date else "N/A"
            time_str = fields.Datetime.to_string(rec.check_in_time) if rec.check_in_time else "N/A"
            rec.name = f"{member_name} - {date_str} {time_str.split(' ')[1]}" # Just time part

    @api.depends('check_in_time', 'check_out_time')
    def _compute_duration(self):
        for rec in self:
            if rec.check_in_time and rec.check_out_time:
                delta = rec.check_out_time - rec.check_in_time
                rec.duration = delta.total_seconds() / 3600.0 # Duration in hours
            else:
                rec.duration = 0.0

    @api.constrains('check_in_time', 'check_out_time')
    def _check_times(self):
        for rec in self:
            if rec.check_in_time and rec.check_out_time and rec.check_in_time >= rec.check_out_time:
                raise ValidationError(_("Check-out time must be after check-in time."))

    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            self.attendance_type = 'class_attendance'
            self.trainer_id = self.class_id.trainer_id.id
            self.check_in_time = self.class_id.start_time
            # self.check_out_time = self.class_id.end_time # Auto-fill checkout time if class has fixed end time

    def action_check_in(self):
        self.ensure_one()
        if not self.check_in_time:
            self.check_in_time = fields.Datetime.now()
        # You might want to add logic here to check for active subscription

    def action_check_out(self):
        self.ensure_one()
        if not self.check_out_time:
            self.check_out_time = fields.Datetime.now()
        if self.check_in_time and self.check_out_time and self.check_in_time >= self.check_out_time:
            raise ValidationError(_("Check-out time must be after check-in time."))

    # Example for QR code check-in (requires frontend integration)
    @api.model
    def check_in_by_qr_code(self, member_id_or_qr_code):
        member = self.env['gym.member'].search([('member_id', '=', member_id_or_qr_code)], limit=1)
        if not member:
            raise ValidationError(_("Member not found."))
        
        # Check for active subscription
        if member.subscription_status != 'active':
            raise ValidationError(_("Member has no active subscription."))
            
        # Create attendance record
        attendance = self.create({
            'member_id': member.id,
            'attendance_type': 'gym_visit',
            'check_in_time': fields.Datetime.now(),
        })
        member.message_post(body=f"Checked in at {attendance.check_in_time.strftime('%Y-%m-%d %H:%M')}")
        return attendance

