from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_original_customer = fields.Char(string='Original Customer')
    x_original_ship_date = fields.Date(string='Original Ship Date')
    x_original_cancel_date = fields.Date(string='Original Cancel Date')
    x_original_customer_shipping_address = fields.Text(string='Original Customer Shipping Address')
