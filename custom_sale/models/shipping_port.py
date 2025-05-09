from odoo import models, fields, api

class ShippingPort(models.Model):

    _name = 'shipping.port'
    _description = 'Shipping Port'

    company_id = fields.Many2one(comodel_name='res.company', required=True, index=True, default=lambda self: self.env.company)
    
    name = fields.Char(string='Name')
    desc = fields.Char(string='Description')
    


    