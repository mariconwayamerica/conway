from odoo import fields, models

LINE_FIELDS = [
    'x_factory_style_number',
    'x_item_display_name',
    'x_general_notes',
    'x_color_code',
    'x_brand',
    'x_collection',
    'x_towel_type',
    'x_sales_description',
]


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_factory_style_number = fields.Char(string='Factory Style Number')
    x_item_display_name = fields.Char(string='Item Display Name')
    x_general_notes = fields.Char(string='General Notes')
    x_color_code = fields.Char(string='Color Code')
    x_brand = fields.Char(string='Brand')
    x_collection = fields.Char(string='Collection')
    x_towel_type = fields.Char(string='Towel Type')
    x_sales_description = fields.Char(string='Sales Description')

    def _prepare_invoice_line(self, **optional_values):
        vals = super()._prepare_invoice_line(**optional_values)
        for f in LINE_FIELDS:
            vals[f] = self[f]
        return vals
