"""花季传媒程序入口"""
# pylint: disable=W0611
from random import randint

from pacc.nox import NoxConsole
from pacc.noxProj import HJCM

HJCM(-1)
NoxConsole.remove_all()
NoxConsole.copy(3, nox_name='HJCM')
# NoxConsole.copy(randint(140, 180))

HJCM(0, 'N7T7ET').mainloop()
