"""统一计算中心（Unified Computing Center, UCC）客户端模块"""
import _thread
from json import loads

import websocket


def on_message(client, message):
    """Callback function which is called when received data."""
    print(f'on_message {message} {client}')
    UCCClient.texts = loads(message)
    _thread.start_new_thread(close, tuple([client]))


def on_error(client, error):
    """Callback function which is called when we get error."""
    print(f'on_error {error} {client}')


def on_close(client, close_status_code, close_msg):
    """Callback function which is called when connection is closed."""
    print(f"on_close {client} closed"
          f"close_status_code is {close_status_code} close_msg is {close_msg}")


def close(client):
    """关闭客户端"""
    client.close()


def on_open(client):
    """Callback function which is called at opening websocket."""
    print(f'on_open {client}')
    client.send(UCCClient.msg)


# pylint: disable=too-few-public-methods
class UCCClient:
    """客户器端类"""
    msg = '003001001'
    texts = []

    @classmethod
    def send(cls, msg):
        """发送信息"""
        cls.msg = msg
        ins = websocket.WebSocketApp(
            "ws://127.0.0.1:56/", on_open=on_open, on_message=on_message, on_error=on_error,
            on_close=on_close)
        ins.run_forever()
        print(cls.texts)
        return cls.texts
