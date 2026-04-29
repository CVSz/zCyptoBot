ALTER TABLE data ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation
ON data
USING (tenant_id = current_setting('app.tenant'));
