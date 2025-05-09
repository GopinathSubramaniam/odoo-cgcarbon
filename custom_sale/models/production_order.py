import base64
from odoo import models, fields, api
from odoo.http import UserError

class ProductionOrder(models.Model):
    _name = 'production.order'
    _description = 'Production Order'

    products = fields.Many2many('product.product', string='Products')
    # lead_ids = fields.One2many('crm.lead', 'partner_id', string='Leads')

    name = fields.Char(
        string="Reference",
        required=True, copy=False, readonly=False,
        index='trigram',
        default='New')
    
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True, index=True,
        default=lambda self: self.env.company)
    
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, change_default=True, index=True,
        tracking=1,
        check_company=True)
    
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead',
        domain="[('partner_id', '=', partner_id)]")
    
    customer_po_number = fields.Char(string="Customer Order No")
    remark = fields.Char(string="Remarks")
    
    production_order_line = fields.One2many(
        comodel_name='production.order.line',
        inverse_name='production_order_id',
        string="Production Order Lines",
        copy=True, auto_join=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('new', 'New'),
        ('sent', 'Sent'),
        ('approved', 'Delivered'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    tags = fields.Many2many('crm.tag', string='Tags')

    packing = fields.Char(string="Packing")
    bag_marking  = fields.Char(string="Bag Marking")
    shipment_schedule  = fields.Char(string="Shipment Schedule")

    additional_columns = fields.One2many('production.order.column', 'production_order_id', string='Additional Columns')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('production.order')
            print(sequence)
            if not sequence:
                raise UserError("Please configure a sequence for production.order Model.")

            vals['name'] = f"{sequence}"

        return super(ProductionOrder, self).create(vals)

    def btn_action(self):
        self.ensure_one()

        for rec in self:
            state = self.env.context.get('state', False)
            rec.write({'state': state})

            if state == 'sent':
                pdf_content, _  = self.env['ir.actions.report'].sudo()._render_qweb_pdf('custom_sale.report_production_order_print', [self.id], data = {'doc': self})
                pdf_attachment = base64.b64encode(pdf_content)
                attachment_obj = {
                    'name': f'{self.name}_report.pdf',
                    'datas': pdf_attachment,
                    # 'datas_fname': f'{self.name}_report.pdf',
                    'mimetype': 'application/pdf',
                }
                attachment = self.env['ir.attachment'].create(attachment_obj)

                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Compose Email',
                    'res_model': 'mail.compose.message',
                    'view_mode': 'form',
                    'target': 'new',  # This opens the dialog in a new window
                    'context': {
                        'default_model': 'production.order',  # This specifies that the email is related to crm.lead
                        'default_res_ids': [int(self.id)],    # This is the current lead's ID
                        'default_subject': 'Production Order PDF',
                        'default_body': 'Please find the attached PDF report for the production order.',
                        'default_partner_ids': [(6, 0, [self.partner_id.id])],  # Set the partner (recipient)
                        'default_attachment_ids': [(6, 0, [attachment.id])],  # Optionally add attachments
                    }
                }

    def btn_print(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/po/download/pdf/{self.id}',
            'target': 'blank',
        }

    @api.onchange('lead_id')
    def add_lead_products(self):
        
        for rec in self:
            print('Id = ', rec.id)
            if rec.lead_id and rec.lead_id.products:
                arr = []
                for line in rec.lead_id.products:
                    # val = rec.id
                    # val = str(val).replace('NewId_', '')
                    arr.append((0, 0, {
                        # 'production_order_id': int(val),
                        'product_id': line.id,   
                        'quantity': 1,     
                    }))

                rec.write({'lead_id': rec.lead_id, 'production_order_line': arr})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'production.order',
            'view_mode': 'form',
            'view_id': self.env.ref('custom_sale.production_view_order_form').id,  # Reference to the form view
            'res_id': self.id,  # Refresh the current record
            'target': 'current',  # Open in the current window (same form)
        }
    
    def add_line(self):
        print('add_line :::::::::::::::::::')
        for rec in self:
            rec.additional_columns.append({'production_order_id': self.id, 'key': '', 'value': '' })

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        lead_id = self._context.get('lead_id')
        if lead_id:
            res['lead_id'] = lead_id
        return res


