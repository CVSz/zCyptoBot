package main

import "fmt"

type State struct {
	Latency int
	Load    int
}

func VerifyTransition(prev, next State) bool {
	// Example transition constraint:
	// next.Latency must not exceed prev.Latency by more than 50.
	return next.Latency <= prev.Latency+50
}

func main() {
	prev := State{Latency: 200, Load: 50}
	next := State{Latency: 180, Load: 60}

	ok := VerifyTransition(prev, next)
	fmt.Println("Valid:", ok)
}
