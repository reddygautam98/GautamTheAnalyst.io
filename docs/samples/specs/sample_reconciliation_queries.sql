-- PayTrack Payment Reconciliation & Validation Sample Queries
-- Fictional case study sample: PayTrack reconciliation engine daily & ad-hoc validation checks

-- 1. Unmatched Transactions with Reason Classification
SELECT 
    pt.payment_id,
    pt.merchant_reference,
    pt.amount AS internal_amount,
    ge.amount AS gateway_amount,
    pt.currency,
    pt.created_at,
    CASE 
        WHEN ge.gateway_reference IS NULL THEN 'Missing Gateway Event'
        WHEN pt.amount <> ge.amount THEN 'Amount Mismatch'
        WHEN pt.currency <> ge.currency THEN 'Currency Mismatch'
        ELSE 'Status Discrepancy'
    END AS mismatch_reason
FROM PAYMENT_TRANSACTION pt
LEFT JOIN GATEWAY_EVENT ge 
    ON pt.payment_id = ge.payment_id
WHERE pt.status = 'UNMATCHED'
ORDER BY pt.created_at DESC;

-- 2. Orphan Gateway Events (Received at Gateway but missing in internal core system)
SELECT 
    ge.event_id,
    ge.gateway_reference,
    ge.amount,
    ge.currency,
    ge.received_at
FROM GATEWAY_EVENT ge
LEFT JOIN PAYMENT_TRANSACTION pt 
    ON ge.payment_id = pt.payment_id
WHERE pt.payment_id IS NULL;

-- 3. Exception Cases Breaching 4-Hour Triage SLA
SELECT 
    ec.case_id,
    ec.payment_id,
    ec.case_status,
    ec.assigned_to,
    ec.updated_at,
    ROUND(CAST(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - ec.created_at)) / 3600.0 AS numeric), 1) AS hours_open
FROM EXCEPTION_CASE ec
WHERE ec.case_status NOT IN ('RESOLVED', 'CLOSED')
  AND (EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - ec.created_at)) / 3600.0) > 4.0
ORDER BY hours_open DESC;

-- 4. Daily Reconciliation Summary KPIs (Feeds Power BI Executive Dashboard)
SELECT 
    CAST(compared_at AS DATE) AS recon_date,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN match_state = 'MATCHED' THEN 1 ELSE 0 END) AS matched_count,
    SUM(CASE WHEN match_state = 'UNMATCHED' THEN 1 ELSE 0 END) AS unmatched_count,
    ROUND(CAST(100.0 * SUM(CASE WHEN match_state = 'MATCHED' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0) AS numeric), 2) AS match_rate_pct
FROM RECON_RESULT
GROUP BY CAST(compared_at AS DATE)
ORDER BY recon_date DESC;

