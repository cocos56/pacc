from .qq import QQ
from .mm import MM
from .tb import TB


class TLJ:
    def __init__(self, deviceSN):
        # QQ(deviceSN).getUnreadMsg()
        MM(deviceSN).sendURL()
        # TB(deviceSN).reopenApp()
