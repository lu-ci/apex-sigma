@echo off
set "VIRTENV_DIR=sigma.env"

call "virtualenv --python=C:\\Python35\\python.exe %VIRTENV_DIR%"
call "%VIRTENV_DIR%\\Scripts\\activate.bat"
call "pip install -r requirements.txt"