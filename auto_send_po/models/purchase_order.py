import base64
import logging
from datetime import datetime, timedelta

from odoo import api, models

_logger = logging.getLogger(__name__)

# Maps substring (case-sensitive) to recipient email.
# Checked in order — first match wins.
_CUSTOMER_EMAIL_MAP = [
    ('WALMART', 'rockstone.lee@loftex.com.cn'),
    ('Wal-mart', 'rockstone.lee@loftex.com.cn'),
    ('Target', 'mike.li@loftex.com.cn'),
    ('TJX', 'jackie.zhang@loftex.com.cn'),
    ('Costco', 'monica.cui@loftex.com.cn'),
]


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _cron_send_po_by_customer(self):
        """Send confirmed POs from the last 24 hours using the standard Send PO
        email action, routed to the vendor contact based on original customer name."""
        cutoff = datetime.now() - timedelta(hours=24)
        orders = self.search([
            ('state', '=', 'purchase'),
            ('date_approve', '>=', cutoff),
        ])

        _logger.info('_cron_send_po_by_customer: found %d orders since %s', len(orders), cutoff)

        template = self.env['mail.template'].search([
            ('name', '=', 'Purchase: Purchase Order'),
            ('model', '=', 'purchase.order'),
        ], limit=1)
        if not template:
            template = self.env.ref('purchase.email_template_edi_purchase', raise_if_not_found=False)
        if not template:
            _logger.warning('_cron_send_po_by_customer: no email template found, aborting')
            return

        for order in orders:
            email_to = self._get_email_for_customer(order.x_original_customer)
            if not email_to:
                order.message_post(
                    body=f'Auto Send PO cron: skipped — no email mapping for customer "{order.x_original_customer}"',
                    message_type='comment',
                    subtype_xmlid='mail.mt_note',
                )
                continue

            # Create mail without sending so we can replace the attachment
            mail_id = template.send_mail(
                order.id,
                force_send=False,
                email_values={'email_to': email_to, 'email_cc': False},
            )
            if not mail_id:
                order.message_post(
                    body='Auto Send PO cron: failed to create mail',
                    message_type='comment',
                    subtype_xmlid='mail.mt_note',
                )
                continue

            mail = self.env['mail.mail'].browse(mail_id)

            # The template attaches the RFQ report by default.
            # Replace all template attachments with the confirmed PO report.
            try:
                pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
                    'purchase.action_report_purchase_order',
                    res_ids=[order.id],
                )
                attachment = self.env['ir.attachment'].create({
                    'name': f'{order.name}.pdf',
                    'type': 'binary',
                    'datas': base64.b64encode(pdf_content),
                    'res_model': 'purchase.order',
                    'res_id': order.id,
                    'mimetype': 'application/pdf',
                })
                mail.attachment_ids = [(5, 0, 0), (4, attachment.id)]
            except Exception:
                pass  # fall through and send with whatever the template attached

            mail.send()
            order.message_post(
                body=f'Auto Send PO cron: emailed to {email_to}',
                message_type='comment',
                subtype_xmlid='mail.mt_note',
            )

    @api.model
    def _get_email_for_customer(self, customer_name):
        if not customer_name:
            return False
        for substring, email in _CUSTOMER_EMAIL_MAP:
            if substring in customer_name:
                return email
        return False
