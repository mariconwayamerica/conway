import logging
from odoo import models, api

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        if not self.env.context.get('auto_confirming_sale'):
            for order in orders.filtered(lambda o: o.state in ('draft', 'sent')):
                try:
                    with self.env.cr.savepoint():
                        order.with_context(auto_confirming_sale=True).action_confirm()
                except Exception as e:
                    _logger.warning('auto_confirm_orders: could not confirm SO %s: %s', order.name, e)
        return orders
