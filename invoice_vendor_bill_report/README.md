# Invoice and Vendor Bill Report

Adds **Accounting > Reporting > Statement Reports > Invoice and Vendor Bill**.

One row per customer invoice, showing:
invoice, date, customer, Original Customer PO Number, total, payment status,
sales order, purchase order(s), vendor, and vendor bill(s).

## How links are found
- Invoice -> Sales Order: invoice lines linked to sales order lines (SQL view).
- Sales Order -> PO: `sale.order._get_purchase_orders()` (covers dropship/MTO).
- PO -> Vendor Bills: `purchase.order.invoice_ids`, cancelled bills hidden.
  If a PO has several bills, they all show on the same row.

## Notes
- Read-only SQL view model (`invoice.vendor.bill.report`, `_auto = False`).
- Users need Purchase read access to see the PO / vendor bill columns.
- Filter by month with the "Invoice Date" filter; group by "Invoice Month".
