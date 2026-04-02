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
        to_confirm = self.filtered(lambda o: o.state in ('draft', 'sent'))
        if not to_confirm:
            return True
        last_po_id = self.env['purchase.order'].search([], order='id desc', limit=1).id or 0
        res = super(SaleOrder, to_confirm).action_confirm()
        if not self.env.context.get('auto_confirming_purchase'):
            self.env['purchase.order'].flush_model()
            new_purchase_orders = self.env['purchase.order'].search([
                ('id', '>', last_po_id),
                ('state', 'in', ('draft', 'sent')),
            ])
            new_purchase_orders.with_context(auto_confirming_purchase=True).button_confirm()
        return res
