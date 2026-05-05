package audit

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"time"
)

type Event struct {
	EventType  string            `json:"event_type"`
	TraceID    string            `json:"trace_id"`
	TenantID   string            `json:"tenant_id"`
	KeyID      string            `json:"key_id"`
	Outcome    string            `json:"outcome"`
	Reason     string            `json:"reason,omitempty"`
	Attributes map[string]string `json:"attributes,omitempty"`
	Timestamp  time.Time         `json:"timestamp"`
}

type Client struct {
	Endpoint string
	HTTP     *http.Client
}

func (c Client) Emit(ctx context.Context, event Event) error {
	if c.Endpoint == "" {
		return nil
	}
	event.Timestamp = time.Now().UTC()
	body, err := json.Marshal(event)
	if err != nil {
		return err
	}
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, c.Endpoint, bytes.NewReader(body))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	client := c.HTTP
	if client == nil {
		client = http.DefaultClient
	}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	return nil
}
