package client

import (
	"ItsBagelBot/apps/ingress/internal/domain"
	"context"
	"sync"

	"go.uber.org/zap"
)

type ConduitManager struct {
	conduitID   string
	shardCount  int
	supervisors map[int]*ShardSupervisor

	publisher domain.Publisher

	shardMod  int
	managerID int
}

const (
	maxShards = 10
)

func NewConduitManager(conduitID string, id int, publisher domain.Publisher) *ConduitManager {
	return &ConduitManager{
		conduitID:   conduitID,
		shardCount:  maxShards,
		supervisors: make(map[int]*ShardSupervisor, maxShards),
		publisher:   publisher,
		managerID:   id,
	}
}

func (c *ConduitManager) Run(ctx context.Context) {
	var wg sync.WaitGroup

	for i := 0; i < c.shardCount; i++ {
		shard := NewShardSupervisor(i, c)
		shard.Publisher = c.publisher
		c.supervisors[i] = shard

		wg.Add(1)
		go func(s *ShardSupervisor) {
			defer wg.Done()
			if err := s.Run(ctx); err != nil {
				zap.L().Error("Shard supervisor exited with error", zap.Int("shard", s.ShardID), zap.Error(err))
			}
		}(shard)
	}

	wg.Wait()
}

func (c *ConduitManager) UpdateTwitchConduit(shardID int, sessionID string) error {
	zap.L().Info("Updating Twitch conduit",
		zap.String("conduit_id", c.conduitID),
		zap.Int("shard_id", shardID),
		zap.String("session_id", sessionID),
	)
	// Implementation logic for updating external Twitch API would go here
	return nil
}
