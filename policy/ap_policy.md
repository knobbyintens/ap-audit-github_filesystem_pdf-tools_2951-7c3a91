# Accounts Payable Invoice Review Policy - FY2026 Q4

Effective date: 2026-10-01
Owner: Corporate Controller

This policy governs the pre-payment review of vendor invoices received by the
central accounts payable desk.

## 1. Vendor master verification
Every invoice must match exactly one record in `master/vendor_registry.csv`.
Both the printed vendor name (case-insensitive, trimmed) and the printed Tax ID
must match the same registry row. A vendor that cannot be matched is
`unregistered_vendor` (severity: high).

## 2. Blocked vendors
An invoice from a vendor whose `risk_tier` is `blocked` is `vendor_blocked`
(severity: high), regardless of amount.

## 3. Duplicate invoices
If the invoice number already appears in `history/payment_history.csv` under any
status, the invoice is `duplicate_invoice` (severity: high).

## 4. Probation vendors
Vendors with `risk_tier` of `probation` are not auto-approved above USD 2,500.00.
If the invoice total is greater than 2,500.00, the invoice is
`probation_limit_exceeded` (severity: medium).

## 5. Invoice arithmetic
The printed TAX must equal 8.0% of SUBTOTAL, rounded to cents (tolerance
USD 0.02), and SUBTOTAL + TAX must equal TOTAL DUE (tolerance USD 0.02).
Any inconsistency is `amount_mismatch` (severity: medium).

## 6. Approval authority
For vendors with `risk_tier` of `approved`, any invoice total above
USD 10,000.00 requires manager approval: `manager_approval_required`
(severity: medium).

## 7. Rule precedence
Evaluate the rules in this order and report the first rule that applies:
1. unregistered_vendor
2. vendor_blocked
3. duplicate_invoice
4. probation_limit_exceeded
5. amount_mismatch
6. manager_approval_required

If none of the rules apply, the invoice is `approved` (no rule, no severity).

## 8. Exception handling
Every flagged invoice must be recorded as an exception item in the shared
workspace and routed to the accounts payable manager for resolution before any
payment is released.
