# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WorkoutPlans(models.Model):
     _name = 'workout.plans'
     _description = 'workout plans'

     name = fields.Char(string="Plan Name", required=True)
     goal = fields.Char(string="Goal", required=True)
    # parent = fields.Char(string="Parent Plan")
     repeat = fields.Char(string="Repeat")
     start_date = fields.Datetime(string='Start Date')
     end_date = fields.Datetime(string='End Date')
     comments = fields.Text(string='Trainer Comments')
     rout_ids = fields.One2many('workout.line','plan_id', string='workout Schedule')

class WorkoutLine(models.Model):
     _name = 'workout.line'
     _description = 'workout line'

     task = fields.Char(string="Task Name")
     sets = fields.Integer(string='Sets')

     rest_time = fields.Char(string='Rest Time')
     exercise = fields.Char(string="Exercise")
     repeats = fields.Integer(string="Repeat")
     plan_id = fields.Many2one('workout.plans')
     day = fields.Selection([
          ('saturday', 'Saturday'),
          ('sunday', 'Sunday'),
          ('monday', 'Monday'),
          ('tuesday', 'Tuesday'),
          ('wednesday', 'Wednesday'),
          ('thursday', 'Thursday'),
          ('friday', 'Friday'),
     ], string='Day', required=True)


