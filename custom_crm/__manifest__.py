{
    "name": "Custom CRM",
    "version": "18.0.1.0",
    "author": "Sygmetiv",
    "website": "https://www.sygmetiv.com",
    "depends": ['base_setup','web', 'sale', 'sale_crm'],
    "data": [
        'security/ir.model.access.csv',
        'views/crm_template.xml'
    ],
    'assets':{
        'web.assets_backend': [
            'custom_crm/static/src/**/*'
        ]
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3'
}
