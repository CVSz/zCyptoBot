package zypto.authz

default allow = false

# input:
# {
#   "principal": {"tenant_id": "A", "roles": ["user"]},
#   "resource":  {"tenant_id": "A", "type": "order"},
#   "action":    "write"
# }

allow {
  input.principal.tenant_id == input.resource.tenant_id
  not forbidden_action
}

forbidden_action {
  input.action == "admin"
  not "admin" in input.principal.roles
}
