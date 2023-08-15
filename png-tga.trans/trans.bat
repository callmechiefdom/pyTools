@echo off
echo "start check requirements.txt file"
if exist %cd%\requirements.txt (
   echo "check requirements.txt finish"
) else (
  echo "not exist requirements.txt"
)  
echo "start init env"
SET curdir=%cd%\venv
echo %curdir%
if not exist  %curdir% (
 python -m venv ./venv
 echo "finish create venv"
)
call %cd%\venv\Scripts\activate.bat
echo "source env finish"
pip install -r requirements.txt
echo "pwd is : %cd%"
python %cd%\t_trans.py

set/p option=wating for cmd:
if "%option%"=="quit" echo input quit
TIMEOUT /T 3