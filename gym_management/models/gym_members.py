from odoo import models, fields

class MemberInfo(models.Model):
    _inherit = 'res.partner'


    # id_number = fields.Char(string='ID Number')


    
class GymTrainer(models.Model):
    _inherit = 'hr.employee'