from odoo import models

from ._constants import LINE_FIELDS


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_purchase_order_line(
        self, product_id, product_qty, product_uom, company_id, values, po
    ):
        vals = super()._prepare_purchase_order_line(
            product_id, product_qty, product_uom, company_id, values, po
        )
        sale_line_id = values.get('sale_line_id')
        if sale_line_id:
            sale_line = self.env['sale.order.line'].browse(sale_line_id)
            for f in LINE_FIELDS:
                vals[f] = sale_line[f]
        return vals
