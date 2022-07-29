"""客户端模块"""
import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    """Callback function which is called when received data."""
    print(f'{ws} {message}')


def on_error(ws, error):
    """Callback function which is called when we get error."""
    print(f'{ws} {error}')


def on_close(ws):
    """Callback function which is called when connection is closed."""
    print(f"{ws} closed")


def on_open(ws):
    """Callback function which is called at opening websocket."""
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send(f"Hello {i}")
        time.sleep(1)
        ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws_client = websocket.WebSocketApp(
        "ws://127.0.0.1:56/", on_open=on_open, on_message=on_message, on_error=on_error,
        on_close=on_close)
    ws_client.run_forever()
