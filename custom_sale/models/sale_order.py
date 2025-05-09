from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # cif_lome = fields.Char(string="CIF LOME")
    
    tags = fields.Many2many('crm.tag', string='Tags')

    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead',
        domain="[('partner_id', '=', partner_id)]")
    
    validate_days = fields.Selection(
        [('10', '10 Days'), ('15', '15 Days'), ('20', '20 Days'), ('25', '25 Days'), ('30', '30 Days')],
        string='Validate Days',
        default='20',
        required=True,
    )
    
    # mesh_size = fields.Char(string="Mesh Size")
    shipping_term_id = fields.Many2one(comodel_name='shipping.term', string='Shipping Term')
    shipping_port_id = fields.Many2one(comodel_name='shipping.port', string='Shipping Port')

    
    def calculate_total(self):
        for rec in self:
            rec.total_shipping_price = rec.ex_factory + rec.shipping_charge
            rec.fob_in_currency = rec.ship_price_in_currency + rec.cif_durben

    @api.onchange('lead_id')
    def add_lead_products(self):
        for rec in self:
            print('Id = ', rec.id)
            if rec.lead_id and rec.lead_id.products:
                arr = []
                for line in rec.lead_id.products:
                    arr.append((0, 0, {
                        'product_id': line.id,   
                        'product_uom_qty': 1,     
                    }))

                rec.write({'lead_id': rec.lead_id, 'order_line': arr})

        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'sale.order',
        #     'view_mode': 'form',
        #     'view_id': self.env.ref('custom_sale.production_view_order_form').id,  # Reference to the form view
        #     'res_id': self.id,  # Refresh the current record
        #     'target': 'current',  # Open in the current window (same form)
        # }


    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        lead_id = self._context.get('lead_id')
        print('lead_id = ', lead_id)
        if lead_id:
            res['lead_id'] = lead_id
        return res
    
    