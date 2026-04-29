CREATE TABLE events (
  ts DateTime,
  user_id String,
  tenant_id String,
  event String,
  props JSON,
  consent_email UInt8 DEFAULT 0,
  consent_sms UInt8 DEFAULT 0,
  consent_push UInt8 DEFAULT 0
) ENGINE = MergeTree
PARTITION BY toDate(ts)
ORDER BY (tenant_id, user_id, ts);

CREATE TABLE users (
  user_id String,
  tenant_id String,
  created_at DateTime
) ENGINE = MergeTree
ORDER BY (tenant_id, user_id);
