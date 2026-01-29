@echo off
echo Cleaning old builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q *.spec 2>nul
echo Build cache cleaned!
echo.
echo Building with new icon...
pyinstaller --onefile --windowed --icon=app_icon.ico --name "ASB SimpleProxy" proxy_app.py
echo.
echo Build complete!
pause
