import logging
from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        result = super().button_validate()
        self.filtered(
            lambda p: p.state == 'done' and p.sale_id and p.purchase_id
        )._auto_create_sale_invoices()
        return result

    def _auto_create_sale_invoices(self):
        for picking in self:
            so = picking.sale_id
            if so.invoice_status != 'to invoice':
                continue
            try:
                so._create_invoices()
                _logger.info(
                    'Auto-created customer invoice for SO %s triggered by dropship picking %s',
                    so.name, picking.name,
                )
            except Exception:
                _logger.exception(
                    'Failed to auto-create invoice for SO %s from dropship picking %s',
                    so.name, picking.name,
                )
