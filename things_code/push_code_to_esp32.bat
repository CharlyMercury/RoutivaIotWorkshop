@echo off

cd C:\Users\Charly Mercury\Desktop\RoutivaIotWorkshop\things_code

rem Get start time:
for /F "tokens=1-4 delims=:.," %%a in ("%time%") do (
   set /A "start=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
)

set timeout_flash=5
set timeout_restart=5
set timeout_upload_micropython=30
set timeout_duration=90

:: Define your variables
set PUERTO=%1

echo.
echo ----------------------------------------
echo Activating Virtualenvironment
echo ----------------------------------------
echo.
call venv\Scripts\activate

:: Erase flash
echo.
echo ----------------------------------------
echo Erasing Flash
echo ----------------------------------------
echo.
python -m esptool --chip esp32 --port %PUERTO% erase_flash
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after %timeout_duration% seconds. Terminating.
  echo.
) else (
  echo.
  echo Esp32 Flashed Correctly
  echo.
)

:: Flash Micropython to esp32
echo.
echo ----------------------------------------
echo Uploading MicroPython to esp32
echo ----------------------------------------
echo.
python -m esptool --chip esp32 --port %PUERTO% --baud 460800 write_flash -z 0x1000 micropython-v1-23-0.bin
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after %timeout_duration% seconds. Terminating.
  echo.
) else (
  echo.
  echo Micropython Uploaded Correctly
  echo.
)

:: Upload reset_machine.py
echo.
echo ----------------------------------------
echo Uploading reset_machine.py to esp32
echo ----------------------------------------
echo.

ampy --port %PUERTO% put reset_machine.py
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating.
  echo.
) else (
  echo.
  echo reset_machine.py was uploaded correctly
  echo.
)

:: Upload umqttsimple file
echo.
echo ----------------------------------------
echo Uploading umqttsimple to esp32
echo ----------------------------------------
echo.
ampy --port %PUERTO% put umqttsimple.py
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating.
  echo.
) else (
  echo.
  echo umqttsimple uploaded correctly
  echo.
)

:: Upload read_sensor file
echo.
echo ----------------------------------------
echo Uploading read_sensor to esp32
echo ----------------------------------------
echo.
ampy --port %PUERTO% put read_sensor.py
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating.
  echo.
) else (
  echo.
  echo read_sensor uploaded correctly
  echo.
)

:: Upload activate_actuator file
echo.
echo ----------------------------------------
echo Uploading activate_actuator to esp32
echo ----------------------------------------
echo.
ampy --port %PUERTO% put activate_actuator.py
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating.
  echo.
) else (
  echo.
  echo activate_actuator uploaded correctly
  echo.
)

:: Upload alerts file
echo.
echo ----------------------------------------
echo Uploading alerts to esp32
echo ----------------------------------------
echo.
ampy --port %PUERTO% put alerts.py
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating.
  echo.
) else (
  echo.
  echo alerts uploaded correctly
  echo.
)

:: Upload parameters json
echo.
echo ----------------------------------------
echo Uploading parameters.json to esp32
echo ----------------------------------------
echo.
ampy --port %PUERTO% put parameters_configuration.json
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating.
  echo.
) else (
  echo.
  echo parameters.json uploaded correctly
  echo.
)

:: Upload main.py and boot.py
echo.
echo ----------------------------------------
echo Uploading main.py and boot.py to esp32
echo ----------------------------------------
echo.
ampy --port %PUERTO% put main.py boot.py
if %errorlevel% equ 1 (
  echo.
  echo. Process timed out after with Errors.  Terminating.
  echo.
) else (
  echo.
  echo main.py and boot.py uploaded correctly
  echo.
)

:: Reset esp32
echo.
echo ----------------------------------------
echo Restarting esp32
echo ----------------------------------------
echo.
:: ampy --port %PUERTO% run reset_machine.py
:: ampy --port %PUERTO% run reset_machine.py --no-output
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating. Problem rebooting esp32.
  echo.
) else (
  echo.
  echo Esp32 was rebooted correctly
  echo.
)

rem Get end time:
for /F "tokens=1-4 delims=:.," %%a in ("%time%") do (
   set /A "end=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
)

rem Get elapsed time:
set /A elapsed=%end%-%start%

echo.
echo ----------------------------------------
rem Show elapsed time:
set /A hh=elapsed/(60*60*100), rest=elapsed%%(60*60*100), mm=rest/(60*100), rest%%=60*100, ss=rest/100, cc=rest%%100
if %mm% lss 10 set mm=0%mm%
if %ss% lss 10 set ss=0%ss%
if %cc% lss 10 set cc=0%cc%
echo %hh%:%mm%:%ss%.%cc%
echo ----------------------------------------
echo.

deactivate