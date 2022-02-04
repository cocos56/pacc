from pacc.config import Config
from pacc.project import DYFD

Config.setDebug(True)
DYFD('003001002').enterLiveRoom()
