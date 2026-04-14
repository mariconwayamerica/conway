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

        template = self.env.ref('purchase.email_template_edi_purchase', raise_if_not_found=False)
        if not template:
            return

        for order in orders:
            email_to = self._get_email_for_customer(order.x_original_customer)
            if not email_to:
                continue
            template.send_mail(
                order.id,
                force_send=True,
                email_values={
                    'email_to': email_to,
                    'email_cc': False,
                },
            )

    @api.model
    def _get_email_for_customer(self, customer_name):
        if not customer_name:
            return False
        for substring, email in _CUSTOMER_EMAIL_MAP:
            if substring in customer_name:
                return email
        return False
