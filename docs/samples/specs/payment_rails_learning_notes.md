# Payment rails: learning notes (study notes, not project experience)

| Rail | Settlement style | Typical use |
|---|---|---|
| RTGS | Real-time gross, one payment at a time | High-value interbank transfers (RBI minimum applies) |
| NEFT | Deferred net settlement in batches, available 24x7 | Everyday account-to-account transfers |
| IMPS | Instant, 24x7 | Mobile and retail instant transfers |
| UPI | Instant, via virtual payment address | Consumer and merchant payments |
| SWIFT MT to MX | Messaging migration to ISO 20022 | Cross-border payment instructions |

Open questions I am studying: how reconciliation breaks differ between batch (NEFT) and instant (IMPS/UPI) rails, and how MT-to-MX truncation affects remittance data.
