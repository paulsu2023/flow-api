@echo off
chcp 65001 >nul
title 🎨 创作实验室 - 本地服务引擎
color 0B

echo ==============================================================
echo                 正在启动 创作实验室 服务端...
echo ==============================================================
echo.
echo [1/3] 应用网络证书补丁...
copy /Y "venv\Lib\site-packages\certifi\cacert.pem" "%TEMP%\cacert.pem" > nul
set CURL_CA_BUNDLE=%TEMP%\cacert.pem

echo [2/3] 正在拉起内部浏览器端口规划...
:: 使用隐式后台运行一个延迟3秒打开网页的命令，防止服务器没完全启动网页就刷出来了
start /b cmd /c "ping 127.0.0.1 -n 3 > nul && start http://127.0.0.1:8000/manage"

echo [3/3] 核心引擎已启动！(请勿关闭此黑色窗口)
echo --------------------------------------------------------------
echo 提示：关闭此黑色窗口即可彻底停止服务。
echo.

call venv\Scripts\activate.bat
python main.py
pause
