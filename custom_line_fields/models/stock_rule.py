from odoo import models

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


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_purchase_order_line(
        self, product_id, product_qty, product_uom, company_id, values, po
    ):
        vals = super()._prepare_purchase_order_line(
            product_id, product_qty, product_uom, company_id, values, po
        )
        sale_line = values.get('sale_line_id')
        if sale_line:
            for f in LINE_FIELDS:
                vals[f] = sale_line[f]
        return vals
