package zypto.cost

default allow = false

# input:
# {
#   "tenant_id": "A",
#   "request_cost": 12.5,
#   "budget": 100.0,
#   "used": 90.0
# }

allow {
  remaining := input.budget - input.used
  input.request_cost <= remaining
}
