package config

import (
	"fmt"
	"os"
	"strconv"
)

type Config struct {
	Address        string
	Environment    string
	Provider       string
	Threshold      int
	Participants   int
	AuditEndpoint  string
	SpiffeRequired bool
}

func Load() (Config, error) {
	cfg := Config{
		Address:        getenv("TSS_ADDRESS", ":8088"),
		Environment:    getenv("ZEAZ_ENV", "dev"),
		Provider:       getenv("TSS_PROVIDER", "disabled"),
		Threshold:      getenvInt("TSS_THRESHOLD", 2),
		Participants:   getenvInt("TSS_PARTICIPANTS", 3),
		AuditEndpoint:  getenv("AUDIT_ENDPOINT", "http://audit-service.zeaz-system.svc:8080/events"),
		SpiffeRequired: getenvBool("SPIFFE_REQUIRED", true),
	}
	if cfg.Threshold < 1 || cfg.Participants < cfg.Threshold {
		return Config{}, fmt.Errorf("invalid threshold policy: threshold=%d participants=%d", cfg.Threshold, cfg.Participants)
	}
	return cfg, nil
}

func getenv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func getenvInt(key string, fallback int) int {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}
	parsed, err := strconv.Atoi(value)
	if err != nil {
		return fallback
	}
	return parsed
}

func getenvBool(key string, fallback bool) bool {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}
	parsed, err := strconv.ParseBool(value)
	if err != nil {
		return fallback
	}
	return parsed
}
