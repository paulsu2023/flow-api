@echo off
echo ==============================================================
echo 正在应用防中文路径补丁...
copy /Y "venv\Lib\site-packages\certifi\cacert.pem" "%TEMP%\cacert.pem" > nul
set CURL_CA_BUNDLE=%TEMP%\cacert.pem
echo 补丁应用成功！正在启动满血版 API...
echo ==============================================================
call venv\Scripts\activate.bat
python main.py
pause
