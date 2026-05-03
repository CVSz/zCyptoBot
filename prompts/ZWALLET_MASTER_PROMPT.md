# 🧠 MASTER META PROMPT — ZWALLET ECOSYSTEM (FULL STACK)

## 🎯 SYSTEM ROLE (inject once)

```text
You are a Principal Blockchain Architect + Senior Mobile Engineer + Security Auditor.

You must generate production-grade, enterprise-ready systems.

Constraints:
- No placeholders, no pseudo-code
- Must follow Clean Architecture + SOLID
- Must include full error handling, validation, and security controls
- Must be scalable, containerized, and cloud-ready
- Must follow OWASP Mobile Top 10 + Web Top 10
- Use modern stacks only (2025+)

Output format:
- File-based structure
- Fully working code
- Config + infra + deployment included
```

---

## 🧩 MODULE 1 — SYSTEM ARCHITECTURE

```text
Design a full-stack multi-chain crypto wallet ecosystem called "zWallet".

Requirements:
- Android Native App (Kotlin + Jetpack Compose)
- Backend API (Node.js + TypeScript + Fastify or NestJS)
- Blockchain Layer (EVM + Solana + BTC support)
- Swap Engine (DEX aggregator: 1inch / Jupiter / Uniswap routing)
- Secure Key Management (non-custodial, HD wallet)
- Database (PostgreSQL + Redis)
- Message Queue (NATS or Kafka)
- Observability (Prometheus + Grafana + OpenTelemetry)
- Infra (Docker + Kubernetes + Terraform)

Must include:
- System diagram
- Service boundaries
- Data flow (wallet → signing → broadcast)
- Threat model (attack surfaces)

Focus:
- Multi-tenant scalability
- Fault isolation
- Latency optimization for swaps
```

---

## 🔐 MODULE 2 — WALLET CORE (CRYPTO ENGINE)

```text
Generate a full crypto wallet engine supporting:

Chains:
- Ethereum (EVM compatible)
- Solana
- Bitcoin

Features:
- HD Wallet (BIP32/39/44)
- Mnemonic generation + validation
- Address derivation
- Private key encryption (AES-256-GCM)
- Secure keystore

Security:
- Zero plaintext key storage
- Memory wiping after use
- Optional biometric unlock abstraction

Include:
- Signing transactions (EVM, Solana, BTC)
- Gas estimation
- Nonce management
- Replay protection

Output:
- TypeScript crypto module
- Kotlin Android secure wrapper
```

---

## 🔁 MODULE 3 — SWAP ENGINE (DEX AGGREGATOR)

```text
Build a swap engine that aggregates liquidity from:

- 1inch (EVM)
- Uniswap (V2/V3)
- Jupiter (Solana)

Features:
- Best route discovery
- Slippage control
- Price impact calculation
- Multi-hop routing
- Token approval flow

Advanced:
- MEV protection (private RPC / Flashbots)
- Sandwich attack mitigation
- Dynamic gas optimization

Output:
- Backend service (routing engine)
- API endpoints
- Quote + execution pipeline
```

---

## 📱 MODULE 4 — ANDROID APP (KOTLIN)

```text
Generate a full Android app (Kotlin + Jetpack Compose):

Features:
- Wallet creation/import (mnemonic)
- Portfolio dashboard (multi-chain balances)
- Send / Receive crypto
- Swap UI (integrated with backend)
- Transaction history
- Token list with real-time prices

Security:
- Biometric authentication
- Encrypted storage (Android Keystore)
- Root/jailbreak detection
- Anti-tampering checks

Architecture:
- MVVM + Clean Architecture
- Repository pattern
- Offline-first support

Include:
- Full UI screens
- State management
- API integration
```

---

## 🌐 MODULE 5 — BACKEND API

```text
Generate a backend API using:

- Node.js (TypeScript)
- Fastify or NestJS
- PostgreSQL + Prisma
- Redis (caching + rate limiting)

Modules:
- Auth (JWT + device binding)
- Wallet metadata (NOT private keys)
- Transaction indexing
- Swap orchestration
- Token price service

Security:
- Rate limiting
- Input validation (Zod)
- Anti-replay
- Audit logs

Include:
- Full API routes
- Middleware
- Error handling
- Unit + integration tests
```

---

## 🧠 MODULE 6 — REAL-TIME DATA + INDEXER

```text
Build blockchain indexer services:

- EVM (using Alchemy / Infura / self-node)
- Solana RPC
- BTC node or API

Features:
- Track balances
- Monitor transactions
- WebSocket push updates

Optimize:
- Event-driven architecture
- Batch processing
- Idempotent jobs

Output:
- Worker services
- Queue system (NATS/Kafka)
```

---

## 🛡️ MODULE 7 — SECURITY HARDENING

```text
Perform full security implementation:

Mobile:
- Secure storage
- Code obfuscation
- Certificate pinning

Backend:
- OWASP protections
- JWT rotation
- Secrets management (Vault)

Blockchain:
- Signature verification
- Transaction simulation before broadcast

Include:
- Threat model
- Attack scenarios
- Mitigations
```

---

## ⚙️ MODULE 8 — DEVOPS / DEPLOYMENT

```text
Generate full DevOps pipeline:

- Dockerized services
- Kubernetes manifests
- Terraform infra (AWS/GCP)

Include:
- CI/CD (GitHub Actions)
- Auto-scaling (HPA)
- Monitoring (Prometheus + Grafana)
- Logging (ELK stack)

Also:
- Blue/green deployment
- Rollback strategy
```

---

## 💰 MODULE 9 — TOKEN + MULTI-CHAIN SUPPORT

```text
Add full token support:

- ERC20 / ERC721 / ERC1155
- SPL tokens (Solana)
- BTC UTXO handling

Features:
- Token discovery
- Metadata caching
- NFT rendering

Optimization:
- Lazy loading
- Indexed queries
```

---

## 🧠 MODULE 10 — AI + ANALYTICS (OPTIONAL ADVANCED)

```text
Add AI intelligence layer:

- Transaction anomaly detection
- User behavior analytics
- Smart swap recommendations

Stack:
- Python (FastAPI)
- Vector DB (pgvector / Weaviate)

Include:
- Feature pipeline
- Real-time inference API
```

---

## 🚀 MASTER ORCHESTRATION PROMPT (use this last)

```text
Combine all modules into a single cohesive production system.

Requirements:
- Fully wired services
- End-to-end working flow:
  Wallet → Sign → Swap → Broadcast → Index → Display

Output:
- Complete monorepo structure
- All services connected
- Environment configs
- Deployment-ready system

Must be:
- Production-ready
- Scalable to 100k+ users
- Secure by design
```

---

## ⚠️ CRITICAL NOTES (ARCHITECT LEVEL)

- Do NOT centralize private keys → always client-side signing
- Avoid single RPC dependency → use fallback providers
- Swap engine = latency-critical → cache aggressively
- Protect against:
  - Front-running
  - RPC spoofing
  - Phishing UI injection
- Android = weakest layer → harden heavily
