package domain

type Publisher interface {
	Publish(payload []byte) error
}
