CREATE MATERIALIZED VIEW events_daily
ENGINE = SummingMergeTree
PARTITION BY day
ORDER BY (tenant_id, event, day)
AS
SELECT
  tenant_id,
  event,
  toDate(ts) AS day,
  count() AS cnt
FROM events
GROUP BY tenant_id, event, day;
