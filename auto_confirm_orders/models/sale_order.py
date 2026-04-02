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
        res = super(SaleOrder, to_confirm).action_confirm()
        if not self.env.context.get('auto_confirming_purchase'):
            self.env['purchase.order'].flush_model(['origin', 'state'])
            so_names = to_confirm.mapped('name')
            purchase_orders = self.env['purchase.order'].search([
                ('origin', 'in', so_names),
                ('state', 'in', ('draft', 'sent')),
            ])
            # Also catch POs where origin has been extended (e.g. "S/001, S/001, S/001")
            for so_name in so_names:
                purchase_orders |= self.env['purchase.order'].search([
                    ('origin', 'like', so_name + ','),
                    ('state', 'in', ('draft', 'sent')),
                ])
            purchase_orders.with_context(auto_confirming_purchase=True).button_confirm()
        return res
