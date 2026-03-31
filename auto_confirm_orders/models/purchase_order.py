from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        if not self.env.context.get('auto_confirming_purchase'):
            orders.with_context(auto_confirming_purchase=True).filtered(
                lambda o: o.state in ('draft', 'sent')
            ).button_confirm()
        return orders
