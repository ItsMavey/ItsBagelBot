package main

import (
	"ItsBagelBot/apps/ingress/internal/client"
	"ItsBagelBot/pkg/logger"
	"context"
	"os"
	"os/signal"
	"syscall"

	"go.uber.org/zap"
)

func main() {
	env := os.Getenv("ENV")

	l := logger.NewLogger(env)

	l.Debug("Logger Initialized ")

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Initialize dependencies (Publisher is nil/mock for now as per current structure)
	conduitID := os.Getenv("TWITCH_CONDUIT_ID")
	cm := client.NewConduitManager(conduitID, 1, nil)

	go cm.Run(ctx)

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	<-sigChan

	cancel()
	Shutdown()
}

func Shutdown() {
	zap.L().Info("Shutting down...")

	_ = zap.L().Sync()
}
