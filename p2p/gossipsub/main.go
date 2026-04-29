package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	libp2p "github.com/libp2p/go-libp2p"
	pubsub "github.com/libp2p/go-libp2p-pubsub"
)

var topics = []string{"bids", "metrics", "attestations"}

func main() {
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()

	h, err := libp2p.New()
	if err != nil {
		log.Fatalf("create host: %v", err)
	}
	defer h.Close()

	ps, err := pubsub.NewGossipSub(ctx, h)
	if err != nil {
		log.Fatalf("create gossipsub: %v", err)
	}

	topicHandles := make(map[string]*pubsub.Topic)
	subs := make(map[string]*pubsub.Subscription)

	for _, t := range topics {
		topic, err := ps.Join(t)
		if err != nil {
			log.Fatalf("join topic %q: %v", t, err)
		}
		sub, err := topic.Subscribe()
		if err != nil {
			log.Fatalf("subscribe topic %q: %v", t, err)
		}

		topicHandles[t] = topic
		subs[t] = sub

		go func(tp string, s *pubsub.Subscription) {
			for {
				msg, err := s.Next(ctx)
				if err != nil {
					if ctx.Err() == nil {
						log.Printf("subscription error (%s): %v", tp, err)
					}
					return
				}
				fmt.Printf("topic=%s from=%s msg=%s\n", tp, msg.GetFrom().String(), string(msg.Data))
			}
		}(t, sub)
	}

	go func() {
		ticker := time.NewTicker(5 * time.Second)
		defer ticker.Stop()
		for {
			select {
			case <-ctx.Done():
				return
			case <-ticker.C:
				if err := topicHandles["metrics"].Publish(ctx, []byte(`{"latency":120}`)); err != nil {
					log.Printf("publish metrics: %v", err)
				}
			}
		}
	}()

	<-ctx.Done()
	log.Println("gossipsub shutting down")
}
