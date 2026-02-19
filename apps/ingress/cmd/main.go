package main

import (
	"ItsBagelBot/pkg/logger"
	"os"
	"os/signal"
	"syscall"

	"go.uber.org/zap"
)

func main() {
	env := os.Getenv("ENV")

	l := logger.NewLogger(env)

	l.Debug("Logger Initialized ")

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	<-sigChan

	Shutdown()

}

func Shutdown() {
	zap.L().Info("Shutting down...")

	_ = zap.L().Sync()
}
