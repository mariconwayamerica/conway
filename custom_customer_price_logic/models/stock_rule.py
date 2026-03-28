import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_purchase_order_line(
        self, product_id, product_qty, product_uom, company_id, values, po
    ):
        vals = super()._prepare_purchase_order_line(
            product_id, product_qty, product_uom, company_id, values, po
        )

        sale_line_id = values.get('sale_line_id')
        if not sale_line_id:
            return vals

        sale_line = self.env['sale.order.line'].browse(sale_line_id)
        if not sale_line.exists():
            return vals

        original_customer = sale_line.order_id.x_original_customer or ''

        if 'TJX Companies' in original_customer:
            so_price = sale_line.price_unit
            new_price = so_price * 0.5
            _logger.info(
                'custom_customer_price_logic: TJX Companies — '
                'SO price_unit=%s, calculated PO price=%s, vals price_unit before=%s '
                '(product: %s, SO: %s)',
                so_price, new_price, vals.get('price_unit'), product_id.name, sale_line.order_id.name,
            )
            vals['price_unit'] = new_price
            _logger.info(
                'custom_customer_price_logic: TJX Companies — vals price_unit after=%s',
                vals['price_unit'],
            )

        elif 'Wal-mart Canada Corp' in original_customer:
            canada_price = self._get_canada_vendor_price(product_id, po.partner_id)
            if canada_price is not None:
                vals['price_unit'] = canada_price
                _logger.info(
                    'custom_customer_price_logic: Walmart Canada — PO price set to canada price = %s '
                    '(product: %s, SO: %s)',
                    canada_price, product_id.name, sale_line.order_id.name,
                )
            else:
                _logger.warning(
                    'custom_customer_price_logic: Walmart Canada — no canada price found for '
                    'product %s / vendor %s, using default vendor price',
                    product_id.name, po.partner_id.name,
                )

        return vals

    def _get_canada_vendor_price(self, product_id, partner_id):
        """Return the unit price from the vendor supplierinfo line with price_type = 'canada'."""
        supplierinfo = self.env['product.supplierinfo'].search([
            ('product_tmpl_id', '=', product_id.product_tmpl_id.id),
            ('partner_id', '=', partner_id.id),
            ('x_studio_price_type', '=', 'canada'),
        ], limit=1)
        if supplierinfo:
            return supplierinfo.price
        return None
