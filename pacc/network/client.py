"""客户端模块"""
import _thread
import time

import websocket


# pylint: disable=too-few-public-methods
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


def on_open(client):
    """Callback function which is called at opening websocket."""
    # pylint: disable=unused-argument
    def run(*args):
        for i in range(3):
            time.sleep(1)
            client.send(f"Hello {i}")
        time.sleep(1)
        client.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())


class Client:
    """客户器端类"""
    client_ins = websocket.WebSocketApp("ws://127.0.0.1:56/")
    client_ins.close()

    def __init__(self):
        # websocket.enableTrace(True)
        self.__class__.client_ins = websocket.WebSocketApp(
            "ws://127.0.0.1:56/", on_open=on_open, on_message=on_message, on_error=on_error,
            on_close=on_close)
        self.__class__.client_ins.run_forever()


if __name__ == "__main__":
    Client()
