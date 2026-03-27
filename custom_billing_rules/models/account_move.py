import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        result = super().action_post()
        self.filtered(
            lambda m: m.move_type == 'in_invoice'
        )._auto_create_sale_invoices()
        return result

    def _auto_create_sale_invoices(self):
        for bill in self:
            purchase_orders = bill.invoice_line_ids.mapped('purchase_line_id.order_id')
            for po in purchase_orders:
                sale_orders = po.order_line.mapped('move_dest_ids.sale_line_id.order_id')
                for so in sale_orders:
                    if so.invoice_status != 'to invoice':
                        continue
                    try:
                        so._create_invoices()
                        _logger.info(
                            'Auto-created customer invoice for SO %s triggered by vendor bill %s',
                            so.name, bill.name,
                        )
                    except Exception:
                        _logger.exception(
                            'Failed to auto-create invoice for SO %s from vendor bill %s',
                            so.name, bill.name,
                        )
