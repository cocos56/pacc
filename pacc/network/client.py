"""客户端模块"""
import time

import websocket

try:
    import thread
except ImportError:
    import _thread as thread


# pylint: disable=too-few-public-methods
class Client:
    """客户器端类"""


def on_message(client, message):
    """Callback function which is called when received data."""
    print(f'{message} {client}')


def on_error(client, error):
    """Callback function which is called when we get error."""
    print(f'{error} {client}')


def on_close(client):
    """Callback function which is called when connection is closed."""
    print(f"{client} closed")


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
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws_client = websocket.WebSocketApp(
        "ws://127.0.0.1:56/", on_open=on_open, on_message=on_message, on_error=on_error,
        on_close=on_close)
    ws_client.run_forever()
