"""服务器端模块"""
import json
from time import sleep

from websocket_server import WebsocketServer


def new_client(client, server):
    """Called for every client connecting (after handshake)"""
    print(f"New client connected and was given id {client['id']}")
    sleep(3)
    server.send_message_to_all("Hey all, a new client has joined us")


# pylint: disable=unused-argument
def client_left(client, server):
    """Called for every client disconnecting"""
    print(f"Client{client['id']} disconnected")


# pylint: disable=unused-argument
def message_received(client, server, message):
    """Called when a client sends a message"""
    message = json.loads(message)
    if len(message) > 100:
        message = message[:100] + '...'
    print(f"Client({client['id']}) said: {message}")
    print(type(message))


# pylint: disable=too-few-public-methods
class Server:
    """服务器端类"""

    def __init__(self):
        server_ins = WebsocketServer('0.0.0.0', 56)
        server_ins.set_fn_new_client(new_client)
        server_ins.set_fn_client_left(client_left)
        server_ins.set_fn_message_received(message_received)
        print("启动成功")
        server_ins.run_forever()


if __name__ == "__main__":
    Server()
