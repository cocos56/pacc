"""微信视窗版模块"""
import time

import pyautogui
import pyperclip


def send_wechat_msg(person, msg: str):
    """发送微信信息

    :param person: 收信人
    :param msg: 待发送的信息
    """
    msg_split = msg.split('\n')
    msg_li = [msg_split[i:i + 30] for i in range(0, len(msg_split), 30)]
    for single_msg in msg_li:
        send_single_wechat_msg(person, '\n'.join(single_msg))


def send_single_wechat_msg(person, single_msg):
    """发送单条微信信息

    :param person: 收信人
    :param single_msg: 待发送的单条信息
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
    pyperclip.copy(single_msg)
    # 使用快捷键ctrl+v将信息粘贴到微信输入框，按回车发送消息
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)
