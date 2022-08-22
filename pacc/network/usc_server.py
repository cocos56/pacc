"""统一存储中心（Unified Storage Center, USC）服务器端模块"""
from websocket_server import WebsocketServer

from ..config import ServerStatus


# pylint: disable=too-few-public-methods
class USCServer:
    """统一存储中心服务器端类"""
    status = ServerStatus.FREE

    @classmethod
    def mainloop(cls):
        """统一存储中心服务器端类的主循环类函数"""
        server_ins = WebsocketServer('0.0.0.0', 57)
        print("统一存储中心（Unified Storage Center, USC）服务器启动成功")
        server_ins.run_forever()
