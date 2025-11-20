@echo off
set "base=C:\Users\szymo\AppData\Local\PythonManagement\venvs"
if not exist "%base%" exit /b 1

pushd "%base%"
for /d %%D in (*) do rmdir "%%D" /s /q
popd
exit