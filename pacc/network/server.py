"""服务器端模块"""
from websocket_server import WebsocketServer


class Server:
    """服务器端类"""


def new_client(client, server):
    """Called for every client connecting (after handshake)"""
    print(f"New client connected and was given id {client['id']}")
    server.send_message_to_all("Hey all, a new client has joined us")


def client_left(client, server):
    """Called for every client disconnecting"""
    print(f"Client{client['id']} disconnected")


def message_received(client, server, message):
    """Called when a client sends a message"""
    if len(message) > 200:
        message = message[:200] + '..'
    print(f"Client({client['id']}) said: {message}")


if __name__ == "__main__":
    ws_server = WebsocketServer('0.0.0.0', 56)
    ws_server.set_fn_new_client(new_client)
    ws_server.set_fn_client_left(client_left)
    ws_server.set_fn_message_received(message_received)
    print("启动成功")
    ws_server.run_forever()
