{
    'name': 'Custom SO Fields',
    'version': '19.0.1.0.0',
    'summary': 'add custom fields to so po invoice vb',
    'category': 'Sales',
    'author': 'Conway',
    'depends': ['sale', 'purchase', 'account', 'stock', 'purchase_portal'],
    'data': [
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/account_move_views.xml',
        'views/portal_purchase_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
