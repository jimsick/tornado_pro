# coding=utf-8
from message_handler import MessageHandler, MessageWebSocket, SendMessageHandler


message_urls = [
    (r'/message/message', MessageHandler),
    (r'/message/message_websocket', MessageWebSocket),
    (r'/message/send_message', SendMessageHandler),
]