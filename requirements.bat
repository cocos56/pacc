%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"
python -m pip install --upgrade pip
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pause