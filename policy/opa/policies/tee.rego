package zypto.tee

default allow = false

allow {
  input.attested == true
  input.spiffe_id != ""
}
