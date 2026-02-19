package handler

import (
	"strings"
	"time"

	"ItsBagelBot/apps/ingress/internal/domain"

	"github.com/lxzan/gws"
	"github.com/tidwall/gjson"
	"go.uber.org/zap"
)

const (
	KeepAliveWindow = 20 * time.Second
)

type TwitchHandler struct {
	gws.BuiltinEventHandler
	Publisher domain.Publisher
	Connected chan string
	Reconnect chan string
	Closing   chan error
}

func (h *TwitchHandler) OnOpen(socket *gws.Conn) {
	zap.L().Debug("Websocket connected")
	err := socket.SetReadDeadline(time.Now().Add(KeepAliveWindow))
	if err != nil {
		zap.L().Error("failed to set read deadline", zap.Error(err))
	}
}

func (h *TwitchHandler) OnMessage(socket *gws.Conn, message *gws.Message) {

	defer func() { // Return memory to the pool (for gws)
		err := message.Close()

		if err != nil {
			zap.L().Error("failed to close message", zap.Error(err))
		}
	}()

	err := socket.SetReadDeadline(time.Now().Add(KeepAliveWindow))
	if err != nil {
		zap.L().Error("failed to set read deadline", zap.Error(err))
	}

	data := message.Bytes()

	msgType := gjson.GetBytes(data, "metadata.message_type").String()

	switch msgType {

	case "session_welcome":
		h.Connected <- gjson.GetBytes(data, "payload.session.id").String()

	case "session_reconnect":
		url := gjson.GetBytes(data, "payload.session.reconnect_url").String()
		h.Reconnect <- url

	case "notification":

		text := gjson.GetBytes(data, "payload.event.message.text").String()

		if !strings.HasPrefix(text, "!") {
			return
		}

		err := h.Publisher.Publish([]byte(text))
		if err != nil {
			zap.L().Error("failed to publish message", zap.Error(err))
		}

	case "session_keepalive":
		return

	default:
		zap.L().Debug("unknown message type", zap.String("type", msgType))
	}

}

func (h *TwitchHandler) OnClose(socket *gws.Conn, err error) {
	zap.L().Debug("Websocket closed", zap.Error(err))
	h.Closing <- err
}

func (h *TwitchHandler) OnError(socket *gws.Conn, err error) {
	zap.L().Error("Websocket error", zap.Error(err))
	h.Closing <- err
}
