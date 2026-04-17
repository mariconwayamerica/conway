{
    'name': 'Auto Confirm Orders',
    'version': '19.0.1.1.0',
    'summary': 'Auto-confirm sales orders on creation; confirm purchase RFQs via daily scheduled action',
    'category': 'Sales/Purchase',
    'author': 'Conway',
    'depends': ['sale', 'purchase', 'purchase_stock', 'custom_line_fields'],
    'data': ['data/cron.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
