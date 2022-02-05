import os
from shutil import rmtree


class NoxProj:

    def __init__(self, noxWorkPath=r'D:\Program Files\Nox\bin'):
        self.noxWorkPath = noxWorkPath
        os.chdir(self.noxWorkPath)

    def cleanUIAFiles(self):
        rmtree('%s/CurrentUIHierarchy' % self.noxWorkPath)
