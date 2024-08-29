@echo off
cd /d %~dp0
call venv\Scripts\activate

REM 更新 pip
python -m pip install --upgrade pip

REM 安装依赖
pip install -r requirements.txt
if errorlevel 1 (
    echo 安装依赖失败，尝试单独安装各个包
    pip install selenium
    pip install bs4
    pip install pandas
    pip install flask
    pip install flask_cors
)

REM 运行应用
echo 启动应用...
python app.py

REM 保持窗口打开
pause
