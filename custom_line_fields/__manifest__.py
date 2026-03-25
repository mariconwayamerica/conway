{
    'name': 'Custom Line Fields',
    'version': '19.0.1.0.0',
    'summary': 'Add custom line-level fields to SO, PO, and Invoice lines',
    'category': 'Sales',
    'author': 'Conway',
    'depends': ['sale', 'purchase', 'account', 'stock', 'purchase_sale'],
    'data': [
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/account_move_views.xml',
        'views/purchase_order_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
