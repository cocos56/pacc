from os.path import exists
from os import mkdir
from shutil import rmtree


def createDir(dirPath, removeOldDir=False):
    if removeOldDir and exists(dirPath):
        rmtree(dirPath)
    if not exists(dirPath):
        mkdir(dirPath)
