
from odoo import models, fields, api
import datetime

class CRMLead(models.Model):
    
    _inherit = 'crm.lead'
    _rec_name = 'lead_num' # For displaying the name in the dropdown

    lead_num = fields.Char('Lead Number', compute='_compute_lead_num', store=True)
    products = fields.Many2many('product.product', string='Products')

    def __str__(self):
        return f"{self.lead_num} - {self.name}"

    @api.depends('name', 'partner_name')
    def _compute_lead_num(self):
        for rec in self:
            if rec.id:
                today = datetime.date.today()
                rec.lead_num = f'CGC/{today.year}/'+str(rec.id).zfill(5)

    def name_get(self):
        print('name_get ===========================================')
        result = []
        for record in self:
            # Concatenate name, code, and custom_field to display in dropdown
            display_name = f"{record.lead_num}-{record.name}"
            result.append((record.id, display_name))
        return result
    
    def action_new_sample(self):
        action = self.env["ir.actions.actions"]._for_xml_id("custom_sale.sale_new_sample_action")
        action['context'] = self._prepare_opportunity_quotation_context()
        action['context']['partner_id'] = self.partner_id.id
        action['context']['lead_id'] = self.id
        return action
    
    def action_new_production_order(self):
        action = self.env["ir.actions.actions"]._for_xml_id("custom_sale.new_production_order_action")
        action['context'] = self._prepare_opportunity_quotation_context()
        action['context']['partner_id'] = self.partner_id.id
        action['context']['lead_id'] = self.id
        return action
    
    def action_sale_quotations_new(self):
        action = super().action_sale_quotations_new()
        action['context']['lead_id'] = self.id
        
        # context = dict(action.get('context', {}))
        # context.update({'lead_id': self.id})
        # action['context'] = context

        return action

        

       
    



    
    