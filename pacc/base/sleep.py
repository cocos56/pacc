"""睡眠模块"""
import time


def sleep(seconds, show_process=True, show_result=True):
    """睡眠

    :param seconds: 睡眠的秒数
    :param show_process: 是否显示睡眠时等待的过程
    :param show_result: 是否显示睡眠的结果
    """
    if not show_process:
        time.sleep(seconds)
    else:
        rest_seconds = seconds
        while rest_seconds > 0:
            print(f'还剩{rest_seconds}秒', end="")
            time.sleep(1)
            print("\r", end="", flush=True)
            rest_seconds -= 1
    if show_result:
        print(f'已完成{seconds}秒的休息')
