{
    "name": "Custom Sale",
    "version": "18.0.1.0",
    "author": "Sygmetiv",
    "website": "https://www.sygmetiv.com",
    "depends": ['base', 'web', 'account', 'sale', 'custom_crm' ],
    "data": [
        'security/ir.model.access.csv',
        'views/sample_template.xml',
        'views/production_order_template.xml',
        'views/template.xml',
        'report/report.xml',
        'report/layouts.xml',
        'report/quotation_pdf.xml',
        'report/sample_pdf.xml',
        'report/production_order_pdf.xml'
    ],
    'installable': True,
    'application': False,
}
