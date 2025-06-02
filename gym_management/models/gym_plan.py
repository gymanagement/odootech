from odoo import models, fields, api, _

class GymWorkoutPlan(models.Model):
    _name = 'gym.workout.plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Gym Workout Plan'

    name = fields.Char(string='Plan Name', required=True)
    member_id = fields.Many2one('gym.member', string='Member', required=True)
    trainer_id = fields.Many2one('gym.trainer', string='Assigned Trainer')
    start_date = fields.Date(string='Start Date', default=fields.Date.today())
    end_date = fields.Date(string='End Date')
    goals = fields.Text(string='Goals')
    
    # Workout routine details (could be a separate one2many for detailed exercises)
    routine_description = fields.Text(string='Workout Routine Description (e.g., exercises, reps, sets)')
    trainer_comments = fields.Text(string='Trainer Comments')

    # Progress tracking (could be a separate one2many for historical progress)
    progress_notes = fields.Text(string='Progress Notes')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    def action_set_active(self):
        self.state = 'active'

    def action_set_completed(self):
        self.state = 'completed'

    def action_set_cancelled(self):
        self.state = 'cancelled'

class GymDietPlan(models.Model):
    _name = 'gym.diet.plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Gym Diet Plan'

    name = fields.Char(string='Plan Name', required=True)
    member_id = fields.Many2one('gym.member', string='Member', required=True)
    trainer_id = fields.Many2one('gym.trainer', string='Assigned Trainer')
    start_date = fields.Date(string='Start Date', default=fields.Date.today())
    end_date = fields.Date(string='End Date')
    goals = fields.Text(string='Goals')
    
    # Diet plan details
    diet_description = fields.Text(string='Diet Plan Description (e.g., meals, calories, macros)')
    trainer_comments = fields.Text(string='Trainer Comments')

    # Progress tracking
    progress_notes = fields.Text(string='Progress Notes')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    def action_set_active(self):
        self.state = 'active'

    def action_set_completed(self):
        self.state = 'completed'

    def action_set_cancelled(self):
        self.state = 'cancelled'

