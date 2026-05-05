package main

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/cvsz/zypto/services/tss-signing/internal/audit"
	"github.com/cvsz/zypto/services/tss-signing/internal/config"
	"github.com/cvsz/zypto/services/tss-signing/internal/signer"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		log.Fatal(err)
	}
	coordinator := signer.Coordinator{Provider: cfg.Provider, Threshold: cfg.Threshold, Participants: cfg.Participants}
	auditClient := audit.Client{Endpoint: cfg.AuditEndpoint}

	http.HandleFunc("/healthz", func(w http.ResponseWriter, _ *http.Request) {
		_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok", "provider": cfg.Provider})
	})

	http.HandleFunc("/v1/sign", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		var req signer.Request
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "invalid json", http.StatusBadRequest)
			return
		}
		resp, err := coordinator.Sign(r.Context(), req)
		outcome := "allow"
		reason := ""
		if err != nil {
			outcome = "deny"
			reason = err.Error()
		}
		_ = auditClient.Emit(r.Context(), audit.Event{EventType: "tss.sign", TraceID: req.TraceID, TenantID: req.TenantID, KeyID: req.KeyID, Outcome: outcome, Reason: reason})
		if err != nil {
			http.Error(w, err.Error(), http.StatusPreconditionRequired)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(resp)
	})

	log.Printf("starting tss signing coordinator on %s provider=%s threshold=%d participants=%d", cfg.Address, cfg.Provider, cfg.Threshold, cfg.Participants)
	log.Fatal(http.ListenAndServe(cfg.Address, nil))
}
