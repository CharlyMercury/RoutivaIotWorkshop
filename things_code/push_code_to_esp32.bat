@echo off

cd C:\Users\Charly Mercury\Desktop\RoutivaIotWorkshop\things_code

set start_time=%TIME%
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

:: Reset esp32
echo.
echo ----------------------------------------
echo Restarting esp32
echo ----------------------------------------
echo.
ampy --port %PUERTO% run reset_machine.py --no-output
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating. Problem rebooting esp32.
  echo.
) else (
  echo.
  echo Esp32 was rebooted correctly
  echo.
)

:: Upload modules directory
echo.
echo ----------------------------------------
echo Uploading modules to esp32
echo ----------------------------------------
echo.
ampy --port %PUERTO% put umqttsimple.py
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating.
  echo.
) else (
  echo.
  echo modules uploaded correctly
  echo.
)

:: Upload main.py and boot.py
echo.
echo ----------------------------------------
echo Uploading main.py and boot.py to esp32
echo ----------------------------------------
echo.
cd src
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
cd C:\Users\Charly Mercury\Desktop\RoutivaIotWorkshop\things_code
ampy --port %PUERTO% run reset_machine.py --no-output
if %errorlevel% equ 1 (
  echo.
  echo Process timed out after with Errors. Terminating. Problem rebooting esp32.
  echo.
) else (
  echo.
  echo Esp32 was rebooted correctly
  echo.
)
