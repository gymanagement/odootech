from odoo import models, fields

class MemberInfo(models.Model):
    _inherit = 'res.partner'

    
class GymTrainer(models.Model):
    _inherit = 'hr.employee'