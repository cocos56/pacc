"""拼多多视频程序入口模块"""
from pacc.config import Config
from pacc.project.pdd_video import PddVideo


Config.set_debug(True)
PddVideo('001001001').mainloop()
