import easyocr


def getTextsFromPic(picPath): return easyocr.Reader(['ch_sim', 'en']).readtext(picPath)
