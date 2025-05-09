from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mesh_size = fields.Char(string="Mesh Size")
    ctc = fields.Char(string="CTC/IV")

    ex_factory = fields.Float(string="Ex Factory")
    shipping_charge = fields.Float(string="FOB")
    shipping_term_inr = fields.Float(string="Total FOB")  
    
    conversion_rate = fields.Float(string="Conversion Rate", default=1)
    converted_price = fields.Float(string="Converted Price")
    shipping_term = fields.Float(string="CIF")

    @api.onchange('ex_factory', 'shipping_charge')
    def calculate_total_shipping_price(self):
        for rec in self:
            rec.shipping_term_inr = rec.ex_factory + rec.shipping_charge

    @api.onchange('conversion_rate', 'converted_price', 'port_charges')
    def calculate_price_total(self):
        for rec in self:
            # rec.converted_price = (rec.shipping_term_inr / rec.conversion_rate) * 1000
            rec.converted_price = (rec.shipping_term_inr * rec.conversion_rate)
            rec.price_unit = rec.converted_price + rec.shipping_term