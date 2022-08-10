"""统一计算中心（Unified Computing Center, UCC）服务器端模块"""
from enum import Enum
from json import dumps
from time import sleep

from websocket_server import WebsocketServer

from ..adb import UIAutomator
from ..tools import get_texts_from_pic


# pylint: disable=unused-argument
def new_client(client, server):
    """Called for every client connecting (after handshake)"""
    print(f"New client connected and was given id {client['id']}")


# pylint: disable=unused-argument
def client_left(client, server):
    """Called for every client disconnecting"""
    print(f"Client{client['id']} disconnected")


def message_received(client, server, message):
    """Called when a client sends a message"""
    while UCCServer.status == ServerStatus.BUSY:
        sleep(3)
        print('server is busy')
    UCCServer.status = ServerStatus.BUSY
    print(f"Client({client['id']}) said: {message}")
    server.send_message(client, dumps(get_texts_from_pic(UIAutomator(message).get_screen())))
    UCCServer.status = ServerStatus.FREE


class ServerStatus(Enum):
    """服务器状态枚举类"""
    FREE = 'free'
    BUSY = 'busy'


# pylint: disable=too-few-public-methods
class UCCServer:
    """服务器端类"""

    status = ServerStatus.FREE

    @classmethod
    def mainloop(cls):
        """主循环函数"""
        server_ins = WebsocketServer('0.0.0.0', 56)
        server_ins.set_fn_new_client(new_client)
        server_ins.set_fn_client_left(client_left)
        server_ins.set_fn_message_received(message_received)
        print("启动成功")
        server_ins.run_forever()
