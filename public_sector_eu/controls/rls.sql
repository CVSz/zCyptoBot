ALTER TABLE data ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_policy
ON data
USING (tenant_id = current_setting('app.tenant'));
