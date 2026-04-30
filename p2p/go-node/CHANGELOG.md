# Changelog

## 2026-04-30
- Fixed build break caused by outdated discovery API usage (`routingdiscovery.Advertise` and `routingdiscovery.TTL`).
- Updated advertisement flow to use `p2p/discovery/util.Advertise` with `core/discovery.TTL`.
- Regenerated module dependency checksums and normalized Go module version declaration for compatibility.
