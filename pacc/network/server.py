"""服务器端模块"""
from enum import Enum
from time import sleep

from websocket_server import WebsocketServer

from ..adb import UIAutomator, ADB
from ..tools import get_texts_from_pic


def new_client(client, server):
    """Called for every client connecting (after handshake)"""
    print(f"New client connected and was given id {client['id']}")


# pylint: disable=unused-argument
def client_left(client, server):
    """Called for every client disconnecting"""
    print(f"Client{client['id']} disconnected")


# pylint: disable=unused-argument
def message_received(client, server, message):
    """Called when a client sends a message"""
    while UCCServer.status == ServerStatus.busy:
        sleep(3)
        print('server is busy')
    UCCServer.status = ServerStatus.busy
    print(f"Client({client['id']}) said: {message}")
    ADB(message).keep_online()
    server.send_message(client, get_texts_from_pic(UIAutomator(message).get_screen()))
    UCCServer.status = ServerStatus.free


class ServerStatus(Enum):
    free = 'free'
    busy = 'busy'


# pylint: disable=too-few-public-methods
class UCCServer:
    """服务器端类"""

    status = ServerStatus.free

    @classmethod
    def mainloop(cls):
        server_ins = WebsocketServer('0.0.0.0', 56)
        server_ins.set_fn_new_client(new_client)
        server_ins.set_fn_client_left(client_left)
        server_ins.set_fn_message_received(message_received)
        print("启动成功")
        server_ins.run_forever()
