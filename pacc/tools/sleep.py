import time


def sleep(seconds, showProcess=True, showResult=True):
    if not showProcess:
        time.sleep(seconds)
    else:
        s = seconds
        while s > 0:
            print('还剩%s秒' % s, end="")
            time.sleep(1)
            print("\r", end="", flush=True)
            s -= 1
    if showResult:
        print('已完成%s秒的休息' % seconds)
