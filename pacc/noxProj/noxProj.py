import os
from shutil import rmtree


class NoxProj:

    def __init__(self, noxWorkPath=r'D:\Program Files\Nox\bin'):
        os.chdir(noxWorkPath)
        rmtree('%s/CurrentUIHierarchy' % noxWorkPath)
