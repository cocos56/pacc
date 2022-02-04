from pacc.project import PDD
from pacc.config import Config

Config.setDebug(True)
PDD('005001001').contactHumanService()
