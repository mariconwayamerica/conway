from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_original_customer = fields.Char(string='Original Customer')
    x_original_customer_po_number = fields.Text(string='Original Customer PO Number')
    x_original_ship_date = fields.Date(string='Original Ship Date')
    x_original_cancel_date = fields.Date(string='Original Cancel Date')
    x_original_customer_shipping_address = fields.Text(string='Original Customer Shipping Address')

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        vals['x_original_customer'] = self.x_original_customer
        vals['x_original_customer_po_number'] = self.x_original_customer_po_number
        vals['x_original_ship_date'] = self.x_original_ship_date
        vals['x_original_cancel_date'] = self.x_original_cancel_date
        vals['x_original_customer_shipping_address'] = self.x_original_customer_shipping_address
        return vals
