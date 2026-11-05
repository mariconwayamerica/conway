from odoo import api, fields, models, tools


class InvoiceVendorBillReport(models.Model):
    """One row per customer invoice, linked to its sales order, the sales
    order's purchase order(s) and those POs' vendor bills.

    The invoice and sales order come from a SQL view so they can be searched,
    filtered and grouped. Purchase orders and vendor bills are computed in
    Python because the SO -> PO link goes through Odoo's own logic
    (sale.order._get_purchase_orders), which covers dropship/MTO links.
    """
    _name = 'invoice.vendor.bill.report'
    _description = 'Invoice and Vendor Bill Report'
    _auto = False
    _rec_name = 'name'
    _order = 'invoice_date desc, id desc'

    name = fields.Char(string='Invoice Number', readonly=True)
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    invoice_date = fields.Date(string='Invoice Date', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    amount_total = fields.Monetary(string='Invoice Total', readonly=True)
    state = fields.Selection(
        selection='_selection_state', string='Status', readonly=True)
    payment_state = fields.Selection(
        selection='_selection_payment_state', string='Payment Status', readonly=True)
    x_original_customer_po_number = fields.Text(string='Original Customer PO Number', readonly=True)
    sale_order_id = fields.Many2one('sale.order', string='Sales Order', readonly=True)

    purchase_order_ids = fields.Many2many(
        'purchase.order', string='Purchase Order',
        compute='_compute_purchase_links')
    vendor_id = fields.Many2one(
        'res.partner', string='Vendor',
        compute='_compute_purchase_links')
    vendor_bill_ids = fields.Many2many(
        'account.move', string='Vendor Bills',
        compute='_compute_purchase_links')

    @api.model
    def _selection_state(self):
        return self.env['account.move']._fields['state'].selection

    @api.model
    def _selection_payment_state(self):
        return self.env['account.move']._fields['payment_state'].selection

    @api.depends('sale_order_id')
    def _compute_purchase_links(self):
        for line in self:
            purchases = line.sale_order_id._get_purchase_orders()
            line.purchase_order_ids = purchases
            line.vendor_id = purchases.partner_id[:1]
            line.vendor_bill_ids = purchases.invoice_ids.filtered(
                lambda m: m.state != 'cancel')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    am.id AS id,
                    am.id AS invoice_id,
                    am.name AS name,
                    am.invoice_date AS invoice_date,
                    am.partner_id AS partner_id,
                    am.company_id AS company_id,
                    am.currency_id AS currency_id,
                    am.amount_total AS amount_total,
                    am.state AS state,
                    am.payment_state AS payment_state,
                    COALESCE(am.x_original_customer_po_number,
                             so.x_original_customer_po_number) AS x_original_customer_po_number,
                    so.id AS sale_order_id
                FROM account_move am
                LEFT JOIN LATERAL (
                    -- Each invoice comes from one sales order in our flow;
                    -- LIMIT 1 keeps one row per invoice if that ever changes.
                    SELECT s.id, s.x_original_customer_po_number
                    FROM account_move_line aml
                    JOIN sale_order_line_invoice_rel rel ON rel.invoice_line_id = aml.id
                    JOIN sale_order_line sol ON sol.id = rel.order_line_id
                    JOIN sale_order s ON s.id = sol.order_id
                    WHERE aml.move_id = am.id
                    ORDER BY s.id
                    LIMIT 1
                ) so ON TRUE
                WHERE am.move_type = 'out_invoice'
            )
        """)

    def action_open_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
        }
