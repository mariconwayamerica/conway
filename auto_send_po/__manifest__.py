{
    'name': 'Auto Send PO',
    'version': '19.0.1.0.0',
    'summary': 'Automatically email confirmed POs daily based on original customer',
    'category': 'Purchase',
    'author': 'Conway',
    'depends': ['purchase', 'custom_so_fields', 'mail'],
    'data': ['data/cron.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
