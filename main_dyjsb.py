from pacc.config import Config
from pacc.project import DYJSB

Config.setDebug(True)
DYJSB('003001001').openTreasureBox()
DYJSB('003001001').viewAds()
