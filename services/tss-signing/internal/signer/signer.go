package signer

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
)

type Request struct {
	TraceID        string `json:"trace_id"`
	TenantID       string `json:"tenant_id"`
	KeyID          string `json:"key_id"`
	MessageDigest  string `json:"message_digest"`
	Algorithm      string `json:"algorithm"`
	IdempotencyKey string `json:"idempotency_key"`
}

type Response struct {
	SignatureRef string `json:"signature_ref"`
	Algorithm    string `json:"algorithm"`
	Quorum       string `json:"quorum"`
	Digest       string `json:"digest"`
}

type Backend interface {
	Sign(ctx context.Context, req Request) (Response, error)
}

type DisabledBackend struct{}

func (DisabledBackend) Sign(context.Context, Request) (Response, error) {
	return Response{}, errors.New("tss backend disabled: configure TSS_PROVIDER=frost or TSS_PROVIDER=tss-lib with isolated signer nodes")
}

type Coordinator struct {
	Provider     string
	Threshold    int
	Participants int
	Backend      Backend
}

func (c Coordinator) Sign(ctx context.Context, req Request) (Response, error) {
	if req.TenantID == "" || req.KeyID == "" || req.MessageDigest == "" || req.IdempotencyKey == "" {
		return Response{}, errors.New("tenant_id, key_id, message_digest, and idempotency_key are required")
	}
	backend := c.Backend
	if backend == nil {
		backend = DisabledBackend{}
	}
	resp, err := backend.Sign(ctx, req)
	if err != nil {
		return Response{}, err
	}
	resp.Quorum = fmt.Sprintf("%d-of-%d", c.Threshold, c.Participants)
	resp.Digest = stableDigest(req)
	return resp, nil
}

func stableDigest(req Request) string {
	h := sha256.Sum256([]byte(req.TenantID + ":" + req.KeyID + ":" + req.MessageDigest + ":" + req.IdempotencyKey))
	return hex.EncodeToString(h[:])
}
