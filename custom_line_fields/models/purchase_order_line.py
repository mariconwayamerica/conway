import logging

from odoo import api, fields, models

from ._constants import LINE_FIELDS

_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_factory_style_number = fields.Char(string='Factory Style Number')
    x_item_display_name = fields.Char(string='Item Display Name')
    x_general_notes = fields.Char(string='General Notes')
    x_color_code = fields.Char(string='Color Code')
    x_brand = fields.Char(string='Brand')
    x_collection = fields.Char(string='Collection')
    x_towel_type = fields.Char(string='Towel Type')
    x_sales_description = fields.Char(string='Sales Description')

    def _sync_fields_from_sale_line(self, sale_line):
        """Copy custom line fields from a sale order line if not already set."""
        sync_vals = {
            f: sale_line[f]
            for f in LINE_FIELDS
            if sale_line[f] and not self[f]
        }
        if sync_vals:
            super(PurchaseOrderLine, self).write(sync_vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sale_line_id = vals.get('sale_line_id')
            _logger.info(
                'custom_line_fields.PurchaseOrderLine.create: '
                'sale_line_id=%s, vals keys=%s',
                sale_line_id,
                list(vals.keys()),
            )
            if sale_line_id and not any(vals.get(f) for f in LINE_FIELDS):
                sale_line = self.env['sale.order.line'].browse(sale_line_id)
                if sale_line.exists():
                    for f in LINE_FIELDS:
                        if sale_line[f]:
                            vals[f] = sale_line[f]
        return super().create(vals_list)

    def write(self, vals):
        if 'sale_line_id' in vals:
            _logger.info(
                'custom_line_fields.PurchaseOrderLine.write: '
                'sale_line_id=%s, vals keys=%s',
                vals.get('sale_line_id'),
                list(vals.keys()),
            )
        result = super().write(vals)
        if 'sale_line_id' in vals and vals.get('sale_line_id'):
            sale_line = self.env['sale.order.line'].browse(vals['sale_line_id'])
            if sale_line.exists():
                for line in self:
                    line._sync_fields_from_sale_line(sale_line)
        return result

    def _prepare_account_move_line(self, move=False):
        vals = super()._prepare_account_move_line(move)
        for f in LINE_FIELDS:
            vals[f] = self[f]
        return vals
