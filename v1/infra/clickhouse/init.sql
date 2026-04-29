CREATE TABLE IF NOT EXISTS trades (
    tenant String,
    signal String,
    size Float64,
    price Float64,
    sentiment Float64,
    whale Float64,
    ts DateTime DEFAULT now()
) ENGINE = MergeTree()
PARTITION BY tenant
ORDER BY (tenant, ts);
