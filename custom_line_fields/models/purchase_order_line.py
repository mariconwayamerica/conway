from odoo import api, fields, models

from ._constants import LINE_FIELDS


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_factory_style_number = fields.Char(string='Factory Style Number')
    x_item_display_name = fields.Char(string='Item Display Name')
    x_item_upc = fields.Char(string='UPC')
    x_general_notes = fields.Char(string='General Notes')
    x_color_code = fields.Char(string='Color Code')
    x_brand = fields.Char(string='Brand')
    x_collection = fields.Char(string='Collection')
    x_towel_type = fields.Char(string='Towel Type')
    x_sales_description = fields.Char(string='Sales Description')
    x_ufo_porate = fields.Float(string='UFOPOrate')

    def _get_sale_line_from_move_dest(self, vals):
        """Resolve the originating sale.order.line via move_dest_ids."""
        move_dest_ids = vals.get('move_dest_ids')
        if not move_dest_ids:
            return None
        if 'sale_line_id' not in self.env['stock.move']._fields:
            return None
        move_ids = []
        for cmd in move_dest_ids:
            if cmd[0] == 6:   # set / replace
                move_ids.extend(cmd[2])
            elif cmd[0] == 4:  # link
                move_ids.append(cmd[1])
        if not move_ids:
            return None
        for move in self.env['stock.move'].browse(move_ids):
            if move.sale_line_id:
                return move.sale_line_id
        return None

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if any(vals.get(f) for f in LINE_FIELDS):
                continue
            # Try direct sale_line_id first, then fall back to move_dest_ids
            sale_line_id = vals.get('sale_line_id')
            sale_line = (
                self.env['sale.order.line'].browse(sale_line_id)
                if sale_line_id
                else self._get_sale_line_from_move_dest(vals)
            )
            if sale_line and sale_line.exists():
                for f in LINE_FIELDS:
                    if sale_line[f]:
                        vals[f] = sale_line[f]
        return super().create(vals_list)

    def _prepare_account_move_line(self, move=False):
        vals = super()._prepare_account_move_line(move)
        for f in LINE_FIELDS:
            vals[f] = self[f]
        return vals
