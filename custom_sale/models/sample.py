import base64
from odoo import models, fields, api
from odoo.http import UserError

class Sample(models.Model):
    _name = 'sample'
    _description = 'Custom Sample'

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
    
    # remark = fields.Char(string="Remarks")

    sample_line = fields.One2many(
        comodel_name='sample.line',
        inverse_name='sample_id',
        string="Sample Lines",
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

    # Summary: Purpose for which required (Kindly give a brief description)
    # purpose = fields.Char(string="Purpose")
    particle_size_distribution = fields.Char(string="Particle Size Distribution")
    ctc = fields.Char(string="CTC")
    apparent_density = fields.Char(string="Apparent Density")
    moisture = fields.Char(string="Moisture")
    ash_value = fields.Char(string="Ash Value")
    ph_value = fields.Char(string="PH Value")

    # Summary: Required Specification /Special requirements(If any)
    # required_specification = fields.Char(string="Specification")

    # Summary: Minimum quantity of sample to be send
    min_quantity = fields.Float(string="Minimum Quantity")
    product_uom = fields.Many2one(comodel_name='uom.uom', string="Unit", store=True)

    courier_type = fields.Selection([
        ('air', 'Air'),
        ('normal', 'Normal'),
    ], string='Courier Type', default='normal')

    courier_payment_status = fields.Selection([
        ('to_pay', 'To Pay'),
        ('paid', 'Paid'),
    ], string='Courier Payment Status', default='to_pay')

    delivery_date_time  = fields.Datetime(string="Delivery Date & Time", required=True)

    @api.model
    def create(self, vals):
        print("Vals = ",  vals)
        if vals and vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('sample')
           
            if not sequence:
                raise UserError("Please configure a sequence for Custom Model.")

            vals['name'] = f"{sequence}"

        return super(Sample, self).create(vals)

    def btn_action(self):
        self.ensure_one()

        for rec in self:
            state = self.env.context.get('state', False)
            rec.write({'state': state})

            if state == 'sent':
                pdf_content, _  = self.env['ir.actions.report'].sudo()._render_qweb_pdf('custom_sale.report_sample_print', [rec.id], data = {'doc': rec})
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
                        'default_model': 'sample',  # This specifies that the email is related to crm.lead
                        'default_res_ids': [int(self.id)],    # This is the current lead's ID
                        'default_subject': 'Samples PDF Report',
                        'default_body': 'Please find the attached PDF report for the samples',
                        'default_partner_ids': [(6, 0, [self.partner_id.id])],  # Set the partner (recipient)
                        'default_attachment_ids': [(6, 0, [attachment.id])],  # Optionally add attachments
                    }
                }

    def btn_print(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/sample/download/pdf/{self.id}',
            'target': 'blank',
        }
    

    @api.onchange('lead_id')
    def add_lead_products(self):
        
        for rec in self:
            if rec.lead_id and rec.lead_id.products:
                arr = []
                for line in rec.lead_id.products:
                    arr.append((0, 0, {
                        'product_id': line.id,   
                        'quantity': 1,     
                    }))

                rec.write({'lead_id': rec.lead_id, 'sample_line': arr})

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        lead_id = self._context.get('lead_id')
        if lead_id:
            res['lead_id'] = lead_id
        return res