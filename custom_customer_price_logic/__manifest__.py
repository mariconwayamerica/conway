{
    'name': 'Custom Customer Price Logic',
    'version': '19.0.1.0.0',
    'summary': 'DEPRECATED: PO unit price is now set from UFOPOrate (x_ufo_porate) by the auto_confirm_orders cron before confirmation',
    'category': 'Purchase',
    'author': 'Conway',
    'depends': ['purchase_stock', 'custom_so_fields', 'custom_line_fields'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
