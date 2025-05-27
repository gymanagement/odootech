from odoo import models,fields

class SubscriptionManagement(models.Model):
 _inherit = 'sale.order'

name = fields.Many2one('gym.member', string="Member Name")



class SaleOrderInherit(models.Model):
    _inherit = 'sale.order.line'
    
    types = fields.Selection([('monthly','Monthly'),('quartely','Quartely'), ('yearly', 'Yearly')], string="Type the Subscription")







   



    
