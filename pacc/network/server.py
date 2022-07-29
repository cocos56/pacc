"""服务器端模块"""
from websocket_server import WebsocketServer


def new_client(client, server):
    """Called for every client connecting (after handshake)"""
    print(f"New client connected and was given id {client['id']}")
    server.send_message_to_all("Hey all, a new client has joined us")


# pylint: disable=unused-argument
def client_left(client, server):
    """Called for every client disconnecting"""
    print(f"Client{client['id']} disconnected")


# pylint: disable=unused-argument
def message_received(client, server, message):
    """Called when a client sends a message"""
    if len(message) > 200:
        message = message[:200] + '..'
    print(f"Client({client['id']}) said: {message}")


# pylint: disable=too-few-public-methods
class Server:
    """服务器端类"""
    server_ins = WebsocketServer('0.0.0.0', 56)
    server_ins.shutdown()

    def __init__(self):
        self.__class__.server_ins = WebsocketServer('0.0.0.0', 56)
        self.__class__.server_ins.set_fn_new_client(new_client)
        self.__class__.server_ins.set_fn_client_left(client_left)
        self.__class__.server_ins.set_fn_message_received(message_received)
        print("启动成功")
        self.__class__.server_ins.run_forever()


if __name__ == "__main__":
    Server()
