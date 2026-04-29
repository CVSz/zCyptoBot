CREATE TABLE IF NOT EXISTS features_offline (
  tenant String,
  f_latency Float64,
  f_error Float64,
  f_lag Float64,
  f_hour Float64,
  f_budget Float64,
  f_tier Float64,
  f_traffic Float64,
  ts DateTime
) ENGINE=MergeTree ORDER BY (tenant, ts);

CREATE TABLE IF NOT EXISTS feature_baselines (
  tenant String,
  feature String,
  values Array(Float64),
  ts DateTime
) ENGINE=MergeTree ORDER BY (tenant, feature, ts);
