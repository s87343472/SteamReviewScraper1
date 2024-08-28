@echo off
setlocal enabledelayedexpansion

REM 检查虚拟环境是否存在
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo 创建虚拟环境失败,请确保已安装Python。
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 检查是否需要安装依赖
if not exist venv\Scripts\flask.exe (
    echo 安装依赖...
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo 安装依赖失败,请检查网络连接或requirements.txt文件。
        pause
        exit /b 1
    )
)

REM 启动服务器
echo 启动服务器...
python app.py

pause
