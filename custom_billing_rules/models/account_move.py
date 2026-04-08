import logging
from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        result = super().button_validate()
        self.filtered(
            lambda p: p.state == 'done' and p.sale_id and p.purchase_id
        )._auto_dropship_sync()
        return result

    def _auto_dropship_sync(self):
        connector = self.env['netsuite.connector']
        for picking in self:
            so = picking.sale_id

            # 1. Create Odoo invoice
            if so.invoice_status != 'to invoice':
                continue
            try:
                invoices = so._create_invoices()
                invoices.action_post()
                _logger.info(
                    'Auto-created and posted customer invoice for SO %s triggered by dropship picking %s',
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

            po_id = None
            try:
                po_id = connector.netsuite_find_po_id(customer_ref)
            except Exception:
                _logger.exception(
                    'NetSuite PO lookup failed for SO %s (reference %r)',
                    so.name, customer_ref,
                )

            if not po_id:
                _logger.warning(
                    'NetSuite sync skipped for SO %s: no PO matched reference %r',
                    so.name, customer_ref,
                )
                continue

            # 2. Create NetSuite Item Fulfillment (must transform from the Sales Order)
            so_ns_id = None
            try:
                so_ns_id = connector.netsuite_find_so_from_po(po_id)
            except Exception:
                _logger.exception(
                    'NetSuite SO lookup from PO failed for SO %s (reference %r)',
                    so.name, customer_ref,
                )

            if so_ns_id:
                try:
                    connector.netsuite_create_item_fulfillment(so_ns_id)
                except Exception:
                    _logger.exception(
                        'NetSuite Item Fulfillment failed for SO %s (reference %r)',
                        so.name, customer_ref,
                    )
            else:
                _logger.warning(
                    'NetSuite Item Fulfillment skipped for SO %s: could not find linked NS Sales Order from PO %s',
                    so.name, po_id,
                )

            # 3. Create NetSuite Vendor Bill (with Odoo invoice number in memo)
            invoice_name = invoices[:1].name if invoices else so.name
            try:
                connector.netsuite_transform_po_to_bill(po_id, memo=invoice_name)
            except Exception:
                _logger.exception(
                    'NetSuite Vendor Bill failed for SO %s (reference %r)',
                    so.name, customer_ref,
                )
