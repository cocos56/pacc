"""统一计算中心（Unified Computing Center, UCC）服务器端模块"""
from os.path import abspath
from datetime import datetime, timedelta
from enum import Enum
from pickle import dump
from time import sleep

from easyocr import Reader
from websocket_server import WebsocketServer

from ..adb import UIAutomator


# pylint: disable=unused-argument
def new_client(client: dict, server):
    """Called for every client connecting (after handshake)

    :param client: 客户端对象，是一个字典，具体实例如{'id': 2, 'handler':
                <websocket_server.websocket_server.WebSocketHandler object at 0x0000027BE9147970>,
                'address': ('127.0.0.1', 52120)}
    :param server: 服务器端对象
    """
    print(f"New client is : {client}")
    UCCServer.datetime_dic.update({client.get('id'): datetime.now()})


# pylint: disable=unused-argument
def client_left(client: dict, server):
    """Called for every client disconnecting

    :param client: 客户端对象，是一个字典，具体实例如{'id': 2, 'handler':
                <websocket_server.websocket_server.WebSocketHandler object at 0x0000027BE9147970>,
                'address': ('127.0.0.1', 52120)}
    :param server: 服务器端对象
    """
    print(f"Client{client.get('id')} disconnected")
    print(f'本次连接耗时：{datetime.now() - UCCServer.datetime_dic.get(client.get("id"))}\n')
    print(UCCServer.datetime_dic)
    UCCServer.datetime_dic.pop(client.get('id'))


def message_received(client, server, serial_num):
    """Called when a client sends a message

    :param client: 客户端对象
    :param server: 服务器端对象
    :param serial_num: 序列号
    """
    while UCCServer.status == ServerStatus.BUSY:
        sleep(3)
        print(f'server is busy at {UCCServer.client_sn} for '
              f'{datetime.now() - UCCServer.last_datetime}')
        if datetime.now() - UCCServer.last_datetime > timedelta(seconds=16):
            UCCServer.status = ServerStatus.FREE
    UCCServer.status = ServerStatus.BUSY
    UCCServer.client_sn = serial_num
    UCCServer.last_datetime = datetime.now()
    print(f"Client({client['id']}) said: {serial_num}")
    pkl_path = abspath(f'CurrentUIHierarchy/{serial_num}.pkl')
    with open(pkl_path, 'wb') as pkl_file:
        dump(Reader(['ch_sim', 'en']).readtext(UIAutomator(serial_num).get_screen()), pkl_file)
    server.send_message(client, pkl_path)
    print('本次计算耗时')
    UCCServer.status = ServerStatus.FREE


class ServerStatus(Enum):
    """服务器状态枚举类"""
    FREE = 'free'
    BUSY = 'busy'


# pylint: disable=too-few-public-methods
class UCCServer:
    """服务器端类"""
    datetime_dic = {}
    status = ServerStatus.FREE
    client_sn = ''
    last_datetime = datetime.now()

    @classmethod
    def mainloop(cls):
        """主循环函数"""
        server_ins = WebsocketServer('0.0.0.0', 56)
        server_ins.set_fn_new_client(new_client)
        server_ins.set_fn_client_left(client_left)
        server_ins.set_fn_message_received(message_received)
        print("统一计算中心（Unified Computing Center, UCC）服务器启动成功")
        server_ins.run_forever()
