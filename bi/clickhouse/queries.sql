-- D1/D7 retention by signup cohort
WITH cohorts AS (
  SELECT user_id, toDate(created_at) AS cohort_day
  FROM users
),
activity AS (
  SELECT user_id, toDate(ts) AS act_day
  FROM events
  WHERE event = 'login'
),
joined AS (
  SELECT
    c.user_id,
    c.cohort_day,
    a.act_day,
    dateDiff('day', c.cohort_day, a.act_day) AS d
  FROM cohorts c
  LEFT JOIN activity a USING (user_id)
)
SELECT
  cohort_day,
  countDistinctIf(user_id, d = 0) AS d0,
  countDistinctIf(user_id, d = 1) AS d1,
  countDistinctIf(user_id, d = 7) AS d7
FROM joined
GROUP BY cohort_day
ORDER BY cohort_day;
