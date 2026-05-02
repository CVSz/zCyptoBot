from __future__ import annotations

from typing import Dict

DEFAULT_LOCALE = "en"
SUPPORTED_LOCALES = {"en", "es"}

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "dashboard_title": "ZEAZ SaaS Dashboard",
        "latency": "Latency",
        "error": "Error",
        "action": "Action",
        "cost_tick": "Cost (tick)",
        "total_usage": "Total usage",
        "admin_title": "Admin Panel",
        "admin_description": "Manage tenants, roles, policies, and model rollouts.",
        "billing_title": "Billing",
        "billing_description": "Usage metering and invoice status (Stripe-ready skeleton).",
        "tenants_title": "Tenants",
        "tenants_description": "Multi-tenant management and access overview.",
        "control_plane_title": "ZEAZ SaaS Control Plane",
        "tab_dashboard": "Dashboard",
        "tab_admin": "Admin",
        "tab_billing": "Billing",
        "tab_tenants": "Tenants",
    },
    "es": {
        "dashboard_title": "Panel SaaS ZEAZ",
        "latency": "Latencia",
        "error": "Error",
        "action": "Acción",
        "cost_tick": "Costo (intervalo)",
        "total_usage": "Uso total",
        "admin_title": "Panel de Administración",
        "admin_description": "Administra inquilinos, roles, políticas y despliegues de modelos.",
        "billing_title": "Facturación",
        "billing_description": "Medición de uso y estado de facturas (base lista para Stripe).",
        "tenants_title": "Inquilinos",
        "tenants_description": "Gestión multiinquilino y resumen de accesos.",
        "control_plane_title": "Plano de Control SaaS de ZEAZ",
        "tab_dashboard": "Panel",
        "tab_admin": "Administración",
        "tab_billing": "Facturación",
        "tab_tenants": "Inquilinos",
    },
}


def normalize_locale(locale: str | None) -> str:
    if not locale:
        return DEFAULT_LOCALE
    short = locale.split("-")[0].lower()
    if short in SUPPORTED_LOCALES:
        return short
    return DEFAULT_LOCALE


def get_messages(locale: str | None) -> Dict[str, str]:
    return TRANSLATIONS[normalize_locale(locale)]
