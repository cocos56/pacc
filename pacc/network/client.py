"""客户端模块"""
import _thread
import base64
import json

import websocket


def on_message(client, message):
    """Callback function which is called when received data."""
    print(f'on_message {message} {client}')


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


def on_open(client=websocket.WebSocketApp("ws://127.0.0.1:56/")):
    """Callback function which is called at opening websocket."""
    print(f'on_open {client}')
    client.send(Client.msg)
    _thread.start_new_thread(close, tuple([client]))


# pylint: disable=too-few-public-methods
class Client:
    """客户器端类"""
    msg = 'Client'

    def send(self, msg):
        """发送信息"""
        self.__class__.msg = msg
        ins = websocket.WebSocketApp(
            "ws://127.0.0.1:56/", on_open=on_open, on_message=on_message, on_error=on_error,
            on_close=on_close)
        ins.run_forever()

    def send_png_file(self, png_path):
        """发送图片文件"""
        with open(png_path, "rb") as file:  # 转为二进制格式
            base64_data = base64.b64encode(file.read())  # 使用base64进行加密
            json_data = json.dumps(str(base64_data))
            self.send(json_data)


if __name__ == "__main__":
    Client().send_png_file(r'D:\0\icons\github.jpg')
