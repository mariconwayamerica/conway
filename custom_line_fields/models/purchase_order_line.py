from odoo import api, fields, models

from ._constants import LINE_FIELDS


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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sale_line_id = vals.get('sale_line_id')
            if sale_line_id and not any(vals.get(f) for f in LINE_FIELDS):
                sale_line = self.env['sale.order.line'].browse(sale_line_id)
                for f in LINE_FIELDS:
                    if sale_line[f]:
                        vals[f] = sale_line[f]
        return super().create(vals_list)

    def _prepare_account_move_line(self, move=False):
        vals = super()._prepare_account_move_line(move)
        for f in LINE_FIELDS:
            vals[f] = self[f]
        return vals
