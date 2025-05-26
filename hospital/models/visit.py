from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Visit(models.Model):

    _name = "hospital.visit"
    _sql_constraints = [
        ('number_unique','UNIQUE(number)',
         'The number must be unique!! you entered an existing visit number, Please enter a different visit number ')
        ]

    number = fields.Integer()
    patient = fields.Many2one("hospital.patient")
    visit_date = fields.Date()
    doctor = fields.Many2one("hospital.doctor")
    drugs = fields.Many2many("hospital.drug")
    description = fields.Text()
    price = fields.Float()
    state = fields.Selection([
        ("draft","Draft"),
        ("good","Good"),
        ("ill","Ill"),
        ("cancel","Cancel"),
    ],default="draft")

    @api.constrains("visit_date")
    def check_visit_date(self):
        for rec in self:
            if rec.visit_date:
                today = fields.Date.today()
                if rec.visit_date < today:
                    raise ValidationError("The visit date cant be from the past, Please enter a future visit date") 

    def change_state_to_good(self):
        for rec in self:
            rec.state = "good"
    
    def ill(self):
        for rec in self:
            rec.state = "ill"
        
    def cancel(self):
        for rec in self:
            rec.state = "cancel"
    
    def draft(self):
        for rec in self:
            rec.state = "draft"