package transport

import (
	"ItsBagelBot/apps/ingress/internal/client/handler"
	"crypto/tls"
	"time"

	"github.com/lxzan/gws"
	"go.uber.org/zap"
)

const (
	ConnectTimeout = 10 * time.Second
)

type WebSocket struct {
	url  string
	conn *gws.Conn
}

func NewWebsocket(url string) *WebSocket {
	return &WebSocket{
		url: url,
	}
}

func (ws *WebSocket) Start(h *handler.TwitchHandler) error {

	options := &gws.ClientOption{
		Addr:               ws.url,
		TlsConfig:          &tls.Config{InsecureSkipVerify: false},
		ReadBufferSize:     4096,
		ReadMaxPayloadSize: 128 * 1024,
		HandshakeTimeout:   ConnectTimeout,
	}

	client, resp, err := gws.NewClient(h, options)
	if err != nil {
		return err
	}

	if resp != nil && resp.Body != nil {
		defer func() {
			if closeErr := resp.Body.Close(); closeErr != nil {
				zap.L().Warn("failed to close handshake response body", zap.Error(closeErr))
			}
		}()
	}

	ws.conn = client
	return nil
}

func (ws *WebSocket) Close(msg []byte) error {
	if ws.conn != nil {
		return ws.conn.WriteClose(1000, msg)
	}
	return nil
}
