"""统一计算中心（Unified Computing Center, UCC）客户端模块"""
import _thread
from pickle import load
from os import remove

import websocket


def on_message(client, serial_num):
    """Callback function which is called when received data.

    :param client: 客户端对象
    :param serial_num: 序列号
    """
    with open(f'CurrentUIHierarchy/{serial_num}.pkl', 'rb') as pkl_file:
        UCCClient.texts = load(pkl_file)
    remove(f'CurrentUIHierarchy/{serial_num}.pkl')
    _thread.start_new_thread(close, tuple([client]))


def on_error(client, error):
    """Callback function which is called when we get error.

    :param client: 客户端对象
    :param error: 错误信息
    """
    print(f'on_error {error} {client}')
    client.close()


def on_close(client, close_status_code, close_msg):
    """Callback function which is called when connection is closed.

    :param client: 客户端对象
    :param close_status_code: 关闭状态码
    :param close_msg: 关闭信息
    """
    print(f"on_close {client} closed"
          f"close_status_code is {close_status_code} close_msg is {close_msg}")


def close(client):
    """关闭客户端

    :param client: 客户端对象
    """
    client.close()


def on_open(client):
    """Callback function which is called at opening websocket.

    :param client: 客户端对象
    """
    client.send(UCCClient.serial_num)


# pylint: disable=too-few-public-methods
class UCCClient:
    """客户器端类"""
    serial_num = '003001001'
    texts = []

    @classmethod
    def send(cls, serial_num):
        """发送信息

        :param serial_num: 序列号
        """
        cls.serial_num = serial_num
        ins = websocket.WebSocketApp(
            "ws://127.0.0.1:56/", on_open=on_open, on_message=on_message, on_error=on_error,
            on_close=on_close)
        ins.run_forever()
        return cls.texts
