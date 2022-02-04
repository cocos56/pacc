from xml.dom import minidom
from html import unescape


def getXML(filePath): return open(filePath, 'r', encoding='utf-8').read()


def prettyXML(filePath):
    xml = getXML(filePath)
    xml = minidom.parseString(xml)
    xml = xml.toprettyxml()
    xml = unescape(xml)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.writelines(xml)
    return xml
