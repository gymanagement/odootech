from odoo import models, fields, api, _

class GymTrainer(models.Model):
    _name = 'gym.trainer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Gym Trainer'

    name = fields.Char(string='Trainer Name', required=True, tracking=True)
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Phone Number', tracking=True)
    expertise = fields.Char(string='Expertise (e.g., Yoga, HIIT, Weightlifting)')
    certifications = fields.Text(string='Certifications')
    bio = fields.Text(string='Biography')
    image_1920 = fields.Image(string="Image", max_width=1920, max_height=1920)

   # A trainer can be assigned to workout/diet plans or classes
    workout_plan_ids = fields.One2many('gym.workout.plan', 'trainer_id', string='Managed Workout Plans')
    diet_plan_ids = fields.One2many('gym.diet.plan', 'trainer_id', string='Managed Diet Plans')
    class_ids = fields.One2many('gym.class', 'trainer_id', string='Scheduled Classes')

    # Trainer schedule (can be complex, simplified for now)
    schedule_notes = fields.Text(string='Schedule Notes')

    # Performance feedback (can be a separate model if detailed feedback is needed)
    feedback_notes = fields.Text(string='Performance Feedback')

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Trainer email must be unique!'),
    ]
