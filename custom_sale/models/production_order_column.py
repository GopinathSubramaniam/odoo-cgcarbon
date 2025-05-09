from odoo import models, fields, api

class ProductionOrderLine(models.Model):
    _name = 'production.order.column'
    _description = 'Production Order Column'

    production_order_id = fields.Many2one( comodel_name='production.order', string="PO Reference", required=True, 
                                          ondelete='cascade', index=True, readonly=True)

    key = fields.Char(string="Label")
    value = fields.Char(string="Value")
    
    

    