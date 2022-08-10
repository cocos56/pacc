"""统一计算中心（Unified Computing Center, UCC）服务器端模块"""
from enum import Enum
from pickle import dump
from time import sleep

from easyocr import Reader
from websocket_server import WebsocketServer

from ..adb import UIAutomator


# pylint: disable=unused-argument
def new_client(client, server):
    """Called for every client connecting (after handshake)

    :param client: 客户端对象
    :param server: 服务器端对象
    """
    print(f"New client connected and was given id {client['id']}")


# pylint: disable=unused-argument
def client_left(client, server):
    """Called for every client disconnecting

    :param client: 客户端对象
    :param server: 服务器端对象
    """
    print(f"Client{client['id']} disconnected")


def message_received(client, server, serial_num):
    """Called when a client sends a message

    :param client: 客户端对象
    :param server: 服务器端对象
    :param serial_num: 序列号
    """
    while UCCServer.status == ServerStatus.BUSY:
        sleep(3)
        print('server is busy')
    UCCServer.status = ServerStatus.BUSY
    print(f"Client({client['id']}) said: {serial_num}")
    dump(Reader(['ch_sim', 'en']).readtext(UIAutomator(serial_num).get_screen()),
         open(f'CurrentUIHierarchy/{serial_num}.pkl', 'wb'))
    server.send_message(client, serial_num)
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
