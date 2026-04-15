import base64
from datetime import datetime, timedelta

from odoo import api, models

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
        """Send confirmed POs created in the last 24 hours to the appropriate
        vendor contact based on the original customer name."""
        cutoff = datetime.now() - timedelta(hours=24)
        orders = self.search([
            ('state', '=', 'purchase'),
            ('date_approve', '>=', cutoff),
        ])

        template = self.env.ref('auto_send_po.email_template_po_auto_send', raise_if_not_found=False)
        if not template:
            return

        for order in orders:
            email_to = self._get_email_for_customer(order.x_original_customer)
            if not email_to:
                continue

            # Render the custom PO PDF and attach it
            attachment = None
            try:
                pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
                    'purchase.action_report_purchase_order',
                    res_ids=[order.id],
                )
                attachment = self.env['ir.attachment'].create({
                    'name': '%s.pdf' % order.name,
                    'type': 'binary',
                    'datas': base64.b64encode(pdf_content),
                    'res_model': 'purchase.order',
                    'res_id': order.id,
                    'mimetype': 'application/pdf',
                })
            except Exception:
                pass

            # Create the mail (not yet sent) then attach the PDF before sending
            mail_id = template.send_mail(
                order.id,
                force_send=False,
                email_values={
                    'email_to': email_to,
                    'email_cc': False,
                },
            )
            if attachment and mail_id:
                self.env['mail.mail'].browse(mail_id).write({
                    'attachment_ids': [(4, attachment.id)],
                })
            self.env['mail.mail'].browse(mail_id).send()

    @api.model
    def _get_email_for_customer(self, customer_name):
        if not customer_name:
            return False
        for substring, email in _CUSTOMER_EMAIL_MAP:
            if substring in customer_name:
                return email
        return False
