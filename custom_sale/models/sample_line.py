from odoo import models, fields, api

class SampleLine(models.Model):
    _name = 'sample.line'
    _description = 'Sample Line Item'

    company_id = fields.Many2one(comodel_name='res.company', required=True, index=True, default=lambda self: self.env.company)
    
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        change_default=True, ondelete='restrict', index='btree_not_null',
        domain="[('sale_ok', '=', True)]")
    
    description = fields.Text( string="Description", store=True, readonly=False)
    quantity = fields.Float(string="Quantity", digits='Quantity', default=1.0, store=True, required=True)
    product_uom = fields.Many2one(comodel_name='uom.uom', string="Unit", store=True)
    sample_id = fields.Many2one( comodel_name='sample', string="Sample Reference", required=True, ondelete='cascade', index=True, copy=False)
    

    