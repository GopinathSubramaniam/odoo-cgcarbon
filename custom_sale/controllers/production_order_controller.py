from odoo import http
from odoo.http import request


class SampleController(http.Controller):

    @http.route('/po/download/pdf/<int:sample_id>', type='http', auth='public')
    def download_pdf(self, sample_id):
        sample_obj = request.env['sample'].browse(sample_id)
        pdf_content, _  = request.env['ir.actions.report'].sudo()._render_qweb_pdf('custom_sale.report_production_order_print', [sample_id], data = {'doc': sample_obj})
        
        pdf_filename = f"production_order.pdf"
        return request.make_response(pdf_content, [
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', f'inline; filename={pdf_filename}')
        ])