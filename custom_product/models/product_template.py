
from odoo import models, fields, api

class ProductTemplate(models.Model):
    
    _inherit = 'product.template'

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


    