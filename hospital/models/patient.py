from odoo import models,fields,api

class Patient(models.Model):

    _name = "hospital.patient"
    _rec_name = "first_name"
    _sql_constraints = [
        ('price_check','CHECK(price >= 0)',
         'The price is not a positive flaot, Please Enter a positive price ')
        ]
    
    first_name = fields.Char(required=True)
    last_name = fields.Char()
    number = fields.Integer()
    price = fields.Float() #readonly=True
    follow_up = fields.Boolean(copy=False)            
    image = fields.Binary()
    status = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'On Progress'),
        ('finish', 'Finish')
    ])
    birthdate = fields.Date()
    age = fields.Integer(compute="_cal_age",store=True)
    age2 =fields.Integer()
    registeration = fields.Datetime(default=fields.Datetime.now)
    bio = fields.Text()
    result = fields.Html()
    active = fields.Boolean(default=True)

    visits = fields.One2many("hospital.visit","patient")

    @api.depends("birthdate")
    def _cal_age(self):
        for rec in self:
            if rec.birthdate:
                 rec.age = fields.Date.today().year - rec.birthdate.year
            else:
                rec.age = 0

    @api.onchange("birthdate")
    def onchange_birthdate(self):
        for rec in self:
            if rec.birthdate:
                 rec.age2 = fields.Date.today().year - rec.birthdate.year
            else:
                rec.age2 = 0





