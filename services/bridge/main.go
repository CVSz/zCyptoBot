package main

import (
	"encoding/json"
	"log"
	"net/http"
)

type publishRequest struct {
	Topic   string `json:"topic"`
	Payload string `json:"payload"`
}

func publishHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req publishRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid payload", http.StatusBadRequest)
		return
	}

	// TODO: hook to libp2p pubsub client/daemon.
	_ = req

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func main() {
	http.HandleFunc("/publish", publishHandler)
	log.Println("bridge listening on :8081")
	log.Fatal(http.ListenAndServe(":8081", nil))
}
