"""微信视窗版模块"""
import pyautogui
import pyperclip
import time


def send_wechat_msg(person, msg):
    """发送微信信息

    :param person: 收信人
    :param msg: 待发送的信息
    """
    # 清空剪切板并将目标写入到剪切板
    pyperclip.copy("")
    pyperclip.copy(person)
    # 打开微信窗
    pyautogui.hotkey("ctrl", "alt", "w")
    time.sleep(1)
    # 使用快捷键ctrl+f定位到微信搜索栏
    pyautogui.hotkey("ctrl", "f")
    time.sleep(1)
    # 使用快捷键ctrl+v将目标粘贴到微信搜索栏，微信将自动搜索
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    # 按回车键打开搜索出的目标
    pyautogui.press("enter")
    time.sleep(1)
    # 清空剪切板并将未点检信息写入到剪切板
    pyperclip.copy("")
    pyperclip.copy(msg)
    # 使用快捷键ctrl+v将信息粘贴到微信输入框，按回车发送消息
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.hotkey("alt", "f4")
