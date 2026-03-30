import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sale_line_id = vals.get('sale_line_id')
            sale_line = (
                self.env['sale.order.line'].browse(sale_line_id)
                if sale_line_id
                else self._get_sale_line_from_move_dest(vals)
            )
            if not (sale_line and sale_line.exists()):
                continue

            original_customer = sale_line.order_id.x_original_customer or ''

            if 'TJX Companies' in original_customer:
                vals['price_unit'] = sale_line.price_unit * 0.93
                _logger.warning(
                    'custom_customer_price_logic: TJX Companies — PO price set to SO * 0.5 = %s '
                    '(SO: %s)',
                    vals['price_unit'], sale_line.order_id.name,
                )

            elif 'Wal-mart Cananda Corp' in original_customer:
                product_id = vals.get('product_id')
                order_id = vals.get('order_id')
                if product_id and order_id:
                    product = self.env['product.product'].browse(product_id)
                    order = self.env['purchase.order'].browse(order_id)
                    canada_price = self._get_canada_vendor_price(product, order.partner_id)
                    if canada_price is not None:
                        vals['price_unit'] = canada_price
                        _logger.warning(
                            'custom_customer_price_logic: Wal-mart Cananda — PO price set to canada price = %s '
                            '(SO: %s)',
                            canada_price, sale_line.order_id.name,
                        )
                    else:
                        _logger.warning(
                            'custom_customer_price_logic: Wal-mart Cananda — no canada price found for '
                            'product %s, using default',
                            product.name,
                        )

        return super().create(vals_list)

    def _get_canada_vendor_price(self, product_id, partner_id):
        supplierinfo = self.env['product.supplierinfo'].search([
            ('product_tmpl_id', '=', product_id.product_tmpl_id.id),
            ('partner_id', '=', partner_id.id),
            ('x_studio_price_type', '=', 'canada'),
        ], limit=1)
        if supplierinfo:
            return supplierinfo.price
        return None
