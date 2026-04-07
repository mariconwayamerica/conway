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
        connector = self.env['netsuite.connector']
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
                continue

            customer_ref = so.client_order_ref
            if not customer_ref:
                _logger.info(
                    'NetSuite sync skipped for SO %s: no Customer Reference set',
                    so.name,
                )
                continue

            try:
                po_id = connector.netsuite_find_po_id(customer_ref)
                if po_id:
                    connector.netsuite_transform_po_to_bill(po_id)
                else:
                    _logger.warning(
                        'NetSuite sync skipped for SO %s: no PO matched reference %r',
                        so.name, customer_ref,
                    )
            except Exception:
                _logger.exception(
                    'NetSuite sync failed for SO %s (reference %r)',
                    so.name, customer_ref,
                )
