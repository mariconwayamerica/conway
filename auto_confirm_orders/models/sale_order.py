from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        if not self.env.context.get('auto_confirming_sale'):
            orders.with_context(auto_confirming_sale=True).filtered(
                lambda o: not o._confirmation_error_message()
            ).action_confirm()
        return orders
