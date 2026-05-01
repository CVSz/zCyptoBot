package zypto.authz

default allow = false

allow {
  input.headers["x-tenant-id"] == input.parsed_body.tenant_id
}
