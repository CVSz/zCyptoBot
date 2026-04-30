# zeaz-p2p node

Minimal libp2p node that boots a DHT instance, starts mDNS discovery, and continuously advertises the `zeaz-network` namespace.

## Run

```bash
cd p2p/go-node
go run .
```

## Verify

```bash
cd p2p/go-node
go test ./...
```
