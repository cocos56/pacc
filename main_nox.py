"""
夜神模拟器程序入口
"""
from pacc.noxProj import HXCCM
from pacc.nox import NoxConsole, getOnlineDevices, NoxADB, NoxUIAutomator

# HXCCM(1).runApp()
# HXCCM(144).mainLoop()
HXCCM(-1)
# NoxConsole.remove(100)
# NoxConsole.copy(100)
# NoxConsole.getNumber()
for i in getOnlineDevices()[0:1]:
    uiaIns = NoxUIAutomator(i)
    # NoxADB(i).getCurrentFocus()
    # uiaIns.getScreen()
    # uiaIns.getCurrentUIHierarchy()
    dic = uiaIns.getDict(contentDesc='跳过')
    print(dic)
