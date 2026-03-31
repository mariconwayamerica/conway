from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        if not self.env.context.get('auto_confirming_sale'):
            orders.with_context(auto_confirming_sale=True).filtered(
                lambda o: o.state == 'draft'
            ).action_confirm()
        return orders

    def action_confirm(self):
        res = super().action_confirm()
        if not self.env.context.get('auto_confirming_purchase'):
            self.flush_recordset()
            self.invalidate_recordset(['procurement_group_id'])
            group_ids = self.filtered(lambda o: o.procurement_group_id).mapped('procurement_group_id').ids
            if group_ids:
                purchase_orders = self.env['purchase.order'].search([
                    ('group_id', 'in', group_ids),
                    ('state', 'in', ('draft', 'sent')),
                ])
                purchase_orders.with_context(auto_confirming_purchase=True).button_confirm()
        return res
