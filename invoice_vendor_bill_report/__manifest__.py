{
    'name': 'Invoice and Vendor Bill Report',
    'version': '19.0.1.0.0',
    'summary': 'One-line view of invoice, sales order, purchase order and vendor bills',
    'category': 'Accounting/Accounting',
    'author': 'Conway',
    'depends': ['account', 'sale_purchase_stock', 'custom_so_fields'],
    'data': [
        'security/ir.model.access.csv',
        'security/invoice_vendor_bill_report_security.xml',
        'report/invoice_vendor_bill_report_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
