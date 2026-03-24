from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_purchase_order(self, company_id, origins, values):
        vals = super()._prepare_purchase_order(company_id, origins, values)
        so = values[0].get('reference_ids') and values[0]['reference_ids'].sale_ids[:1]
        if so:
            vals['x_original_customer'] = so.x_original_customer
            vals['x_original_customer_po_number'] = so.x_original_customer_po_number
            vals['x_original_ship_date'] = so.x_original_ship_date
            vals['x_original_cancel_date'] = so.x_original_cancel_date
            vals['x_original_customer_shipping_address'] = so.x_original_customer_shipping_address
        return vals
