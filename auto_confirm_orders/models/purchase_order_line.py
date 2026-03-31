from odoo import models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        if not self.env.context.get('auto_confirming_purchase'):
            lines.mapped('order_id').filtered(
                lambda o: o.state in ('draft', 'sent')
            ).with_context(auto_confirming_purchase=True).button_confirm()
        return lines
