"""淘宝/拼多多全自动远程刷单程序入口C02模块"""
from pacc.project import SD
from pacc.config import Config

Config.set_debug(True)
SD.mainloop([
    '001021001',  # 闫明星，无法充电
    # '001021002',  # 李文蓉，无ROOT
    '001021003',
    # '001021005',  # 徐其锋，无ROOT
    # '001021007',  # 黎梅华，无ROOT
    # '001024001',  # 徐可可，无ROOT
    # '001101006',  # 李泽坤，待入职
    # '001101008',
])
