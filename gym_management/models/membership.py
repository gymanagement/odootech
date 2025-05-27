from odoo import models,fields

class Membership(models.Model):
    _name = 'membership.membership'

    member_id = fields.Many2one('res.partner', string="Member")
    trainer_id = fields.Many2one('hr.employee', string="Trainer")
    subscription_plan= fields.Char(String="Subscription Plan")
