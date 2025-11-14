from network.listeners.chatListener import ChatListener
from network.listeners.streamStatusListener import StreamStatusListener


LISTENERS = [
    ChatListener(),
    StreamStatusListener(),
]