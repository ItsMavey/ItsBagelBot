package client

type ConduitManager struct {
	conduitID   string
	shardCount  int
	supervisors map[int]*ShardSupervisor

	shardMod  int
	managerID int
}

const (
	maxShards = 10
)

func NewConduitManager(conduitID string, id int) *ConduitManager {
	return &ConduitManager{
		conduitID:   conduitID,
		supervisors: make(map[int]*ShardSupervisor, maxShards),
		managerID:   id,
	}
}

func (c *ConduitManager) Run() {

}

func (c *ConduitManager) UpdateTwitchConduit(shardID int, sessionID string) error {
	return nil
}
