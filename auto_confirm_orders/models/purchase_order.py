from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _cron_confirm_rfq(self):
        orders = self.search([('state', 'in', ('draft', 'sent'))])
        for order in orders:
            for line in order.order_line:
                if line.x_ufo_porate:
                    line.price_unit = line.x_ufo_porate
        orders.button_confirm()
