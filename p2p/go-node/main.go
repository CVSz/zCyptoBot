package main

import (
	"context"
	"fmt"
	"log"
	"time"

	libp2p "github.com/libp2p/go-libp2p"
	dht "github.com/libp2p/go-libp2p-kad-dht"
	discovery "github.com/libp2p/go-libp2p/core/discovery"
	host "github.com/libp2p/go-libp2p/core/host"
	peer "github.com/libp2p/go-libp2p/core/peer"
	mdns "github.com/libp2p/go-libp2p/p2p/discovery/mdns"
	routingdiscovery "github.com/libp2p/go-libp2p/p2p/discovery/routing"
	discoveryutil "github.com/libp2p/go-libp2p/p2p/discovery/util"
)

type mdnsNotifee struct{ h host.Host }

func (n *mdnsNotifee) HandlePeerFound(pi peer.AddrInfo) {
	if err := n.h.Connect(context.Background(), pi); err != nil {
		log.Printf("mdns connect error: %v", err)
	}
}

func main() {
	ctx := context.Background()

	h, err := libp2p.New()
	if err != nil {
		log.Fatalf("failed to init libp2p: %v", err)
	}

	kdht, err := dht.New(ctx, h)
	if err != nil {
		log.Fatalf("failed to init dht: %v", err)
	}

	if err := kdht.Bootstrap(ctx); err != nil {
		log.Fatalf("failed to bootstrap dht: %v", err)
	}

	svc := mdns.NewMdnsService(h, "zeaz-mdns", &mdnsNotifee{h: h})
	if err := svc.Start(); err != nil {
		log.Fatalf("failed to start mdns: %v", err)
	}

	routingDiscovery := routingdiscovery.NewRoutingDiscovery(kdht)
	discoveryutil.Advertise(ctx, routingDiscovery, "zeaz-network", discovery.TTL(time.Minute))

	fmt.Printf("Node ID: %s\n", h.ID().String())
	select {}
}
