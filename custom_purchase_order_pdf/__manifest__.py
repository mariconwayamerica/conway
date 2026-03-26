{
    'name': 'Custom Purchase Order PDF',
    'version': '19.0.1.0.0',
    'summary': 'Adds custom header fields and line columns to the Purchase Order PDF report',
    'category': 'Purchase',
    'author': 'Conway',
    'depends': ['purchase', 'custom_so_fields', 'custom_line_fields'],
    'data': [
        'report/purchase_order_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
