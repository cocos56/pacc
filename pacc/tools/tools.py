import os
import easyocr
from urlextract import URLExtract

extractor = URLExtract()


def system(cmd, isPrint=True):
    if isPrint:
        print(cmd)
    os.system(cmd)


def getTextsFromPic(picPath): return easyocr.Reader(['ch_sim', 'en']).readtext(picPath)


def getURLsFromString(string): return extractor.find_urls(string)


def average(*args): return int(sum(args) / len(args))
