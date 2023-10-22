@echo off
setlocal enabledelayedexpansion

set "config=init.txt"
set "app=AutoWindowArranger.exe"

for /f "delims=" %%a in (!config!) do (
  set "params=%%a"
  start "AutoWindowArranger" "!app!" !params!
)

endlocal