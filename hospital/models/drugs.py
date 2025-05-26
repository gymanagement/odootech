from odoo import models,fields

class Drugs(models.Model):

    _name = "hospital.drug"

    name = fields.Char()
    visits = fields.Many2many("hospital.visit")
    


