package config

type Infra struct {
	Controller string `env:"CONTROLLER_IP"`
}

type Twitch struct {
	Client_ID     string `env:"CLIENT_ID"`
	Client_Secret string `env:"CLIENT_SECRET"`
}
