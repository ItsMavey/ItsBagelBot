package client

import (
	"ItsBagelBot/apps/ingress/internal/client/handler"
	"ItsBagelBot/apps/ingress/internal/client/transport"
	"ItsBagelBot/apps/ingress/internal/domain"
	"context"
	"time"

	"go.uber.org/zap"
)

const (
	TwitchURL = "wss://eventsub.wss.twitch.tv/ws"
)

type Orchestrator interface {
	UpdateTwitchConduit(shardID int, sessionID string) error
}

type ShardSupervisor struct {
	ShardID          int
	currentSessionID string

	Publisher domain.Publisher

	connected chan string
	reconnect chan string
	closing   chan error

	orchestrator Orchestrator
}

func NewShardSupervisor(shardID int, o Orchestrator) *ShardSupervisor {
	return &ShardSupervisor{
		ShardID: shardID,

		connected: make(chan string, 1),
		reconnect: make(chan string, 1),
		closing:   make(chan error, 1),

		orchestrator: o,
	}
}

func (s *ShardSupervisor) createHandler(p domain.Publisher) *handler.TwitchHandler {
	return &handler.TwitchHandler{
		Publisher: p,
		Connected: s.connected,
		Reconnect: s.reconnect,
		Closing:   s.closing,
	}
}

func (s *ShardSupervisor) Run(ctx context.Context) error {
	currentURL := TwitchURL

	var activeConn *transport.WebSocket

	for {

		h := handler.TwitchHandler{
			Publisher: s.Publisher,
			Connected: s.connected,
			Reconnect: s.reconnect,
			Closing:   s.closing,
		}

		newConn := transport.NewWebsocket(currentURL)
		err := newConn.Start(&h)
		if err != nil {
			zap.L().Error("Dial failed, retrying in 5s", zap.Error(err))

			time.Sleep(5 * time.Second)

			currentURL = TwitchURL
			continue
		}

		restart, err := s.monitor(ctx, newConn, &activeConn, &currentURL)
		if err != nil {
			zap.L().Error("Monitor failed, retrying in 5s", zap.Error(err))
			return err
		}

		if !restart {
			return nil
		}
	}
}

func (s *ShardSupervisor) monitor(ctx context.Context, newConn *transport.WebSocket, activeConn **transport.WebSocket, currentURL *string) (bool, error) {
	for {
		select {
		case <-ctx.Done():
			if *activeConn == nil {
				return false, nil
			}

			err := (*activeConn).Close([]byte("shutdown"))
			if err != nil {
				zap.L().Error("failed to close websocket", zap.Error(err))
				return false, err
			}

		case sessionID := <-s.connected:
			s.currentSessionID = sessionID
			zap.L().Info("Session active", zap.Int("shard", s.ShardID), zap.String("id", sessionID))

			s.notifyReady(sessionID)

			if *activeConn != nil {
				zap.L().Debug("Closing old connection after handover", zap.Int("shard", s.ShardID))
				old := *activeConn

				go func() {
					if err := old.Close([]byte("handover complete")); err != nil {
						zap.L().Error("failed to close old websocket", zap.Error(err))
					}
				}()
			}

			*activeConn = newConn

		case nextURL := <-s.reconnect:
			zap.L().Warn("Migration signal received", zap.Int("shard", s.ShardID), zap.String("url", nextURL))
			*currentURL = nextURL

			return true, nil

		case err := <-s.closing:
			zap.L().Error("Socket closed/lost", zap.Int("shard", s.ShardID), zap.Error(err))
			*currentURL = TwitchURL
			return true, nil
		}
	}

}

func (s *ShardSupervisor) notifyReady(sessionID string) {

	zap.L().Info("Notify Ready to Orchestrator")

	err := s.orchestrator.UpdateTwitchConduit(s.ShardID, sessionID)
	if err != nil {
		zap.L().Error("failed to update twitch conduit", zap.Error(err))
	}
}
