从手机向电脑传输文件：
输入:
adb pull 手机存储路径 电脑路径
adb pull /sdcard/xxx /Users/xxxx/xxx

从电脑向手机传输文件：
输入：
adb push 电脑路径 手机存储路径
adb push /Users/xxxx/xxx /sdcard/xxx
adb -s 192.168.1.19 push 137.png /sdcard/Pictures/a.png