%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"
python -m pip install --upgrade pip
pip install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple
pause