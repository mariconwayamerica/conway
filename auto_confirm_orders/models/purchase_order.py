from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _cron_confirm_rfq(self):
        orders = self.search([('state', 'in', ('draft', 'sent'))])
        orders.button_confirm()
