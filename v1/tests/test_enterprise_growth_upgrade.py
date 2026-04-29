from app.enterprise.saas import EnterpriseSaaS
from app.growth.automation import GrowthAutomation


def test_multi_tenant_role_isolation_and_audit() -> None:
    saas = EnterpriseSaaS()
    saas.assign_role("alice", "admin", tenant_id="t1")
    saas.assign_role("bob", "user", tenant_id="t2")

    assert saas.list_roles("t1") == {"alice": "admin"}
    assert saas.list_roles("t2") == {"bob": "user"}
    assert saas.list_roles("t3") == {}

    events_t1 = saas.get_audit_events("t1")
    events_t2 = saas.get_audit_events("t2")
    assert len(events_t1) == 1
    assert len(events_t2) == 1


def test_slo_dashboard_and_growth_analytics() -> None:
    saas = EnterpriseSaaS()
    growth = GrowthAutomation()

    saas.upsert_slo("api-gateway", availability=99.95, p95_latency_ms=120, error_rate=0.002, tenant_id="acme")
    dash = saas.slo_dashboard("acme")
    assert dash["api-gateway"]["availability"] == 99.95

    growth.track_stage("u1", "signup", tenant_id="acme")
    growth.track_stage("u1", "trial", tenant_id="acme")
    growth.track_stage("u2", "signup", tenant_id="acme")

    actions = growth.generate_actions("acme")
    assert any(a["play"] == "activation_nudge" for a in actions)

    analytics = growth.analytics("acme")
    assert analytics["events"] == 3
    assert analytics["active_users"] == 2
