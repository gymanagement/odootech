from odoo import models,fields

class Doctor(models.Model):

    _name = "hospital.doctor"
   
    name = fields.Char()
    
   

  
    