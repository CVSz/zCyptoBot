CREATE TABLE IF NOT EXISTS trades (
    signal String,
    size Float64,
    price Float64,
    ts DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY ts;
