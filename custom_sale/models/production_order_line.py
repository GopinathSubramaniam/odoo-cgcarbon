from odoo import models, fields, api

class ProductionOrderLine(models.Model):
    _name = 'production.order.line'
    _description = 'Production Order Line Item'

    company_id = fields.Many2one(comodel_name='res.company', required=True, index=True, default=lambda self: self.env.company)
    
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        change_default=True, ondelete='restrict', index='btree_not_null',
        domain="[('sale_ok', '=', True)]")
    
    description = fields.Text( string="Description", store=True, readonly=False)
    quantity = fields.Float(string="Quantity", digits='Quantity', default=1.0, store=True, required=True)
    product_uom = fields.Many2one(comodel_name='uom.uom', string="Unit", store=True)
    production_order_id = fields.Many2one( comodel_name='production.order', string="PO Reference", required=True, ondelete='cascade', index=True)

    size = fields.Char(string="Size")
    psd = fields.Char(string="PSD")
    platelets = fields.Char(string="Platelets")
    ctc = fields.Char(string="CTC")
    iodine = fields.Char(string="Iodine")
    surface_area = fields.Char(string="Surface Area")
    moisture = fields.Char(string="Moisture")
    bph = fields.Char(string="BPH")
    ph = fields.Char(string="PH Value")
    ash_content = fields.Char(string="ASH Content")
    bulk_density = fields.Char(string="Bulk Density")
    attrition_loss = fields.Char(string="Attrition Loss")
    k_value = fields.Char(string="K Value")
    r_value = fields.Char(string="R Value")
    

    