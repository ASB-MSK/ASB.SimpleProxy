@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo Building executable...
pyinstaller --noconfirm --onefile --windowed --name "ASB SimpleProxy" --collect-all customtkinter proxy_app.py
echo Build complete. Executable is in the dist folder.
pause
