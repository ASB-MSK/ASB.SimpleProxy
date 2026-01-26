# Implementation Plan - SimpleProxyConnect

## 1. Overview
This is a standalone Windows GUI application to manage system-wide IPv4 proxy settings with authentication support. It uses `customtkinter` for the interface and native Windows libraries (`winreg`, `ctypes`) for system integration.

## 2. Architecture
- **Language**: Python 3.x
- **GUI Framework**: CustomTkinter
- **System API**: `winreg` (Registry), `ctypes` (WinInet), `subprocess` (cmdkey)
- **Distribution**: PyInstaller (One-file executable)

## 3. UI Design (Ref. Image `simple_proxy_connect_ui_mockup`)
- **Theme**: Dark Blue/Gray (CTk 'dark').
- **Layout**:
  - **Header**: Title "SimpleProxyConnect"
  - **Inputs**:
    - IP Address (Entry)
    - Port (Entry, numeric validation recommended)
    - Username (Entry)
    - Password (Entry, show='*')
    - Proxy Type (OptionMenu: 'HTTP', 'HTTPS' - though Windows usually treats them identically in ProxyServer string like `server:port`)
  - **Controls**:
    - Connect Button (Green, large)
    - Disconnect Button (Red, large)
  - **Footer**:
    - Status Label (Color coded: Red/Green)

## 4. Core Logic

### A. Registry Management (`ProxyManager` Class)
Target Key: `HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings`

**Actions:**
1. **Connect**:
   - `ProxyEnable` = `1` (DWORD)
   - `ProxyServer` = `{ip}:{port}` (SZ)
   - `ProxyOverride` = `<local>` (SZ) - bypass local addresses.
   - **Auth**: Execute `cmdkey /add:{ip} /user:{user} /pass:{pass}` to store credentials in Windows Credential Manager. This reduces prompts for system services.
   - **Refresh**: Call `InternetSetOption` to notify the system of changes.

2. **Disconnect**:
   - `ProxyEnable` = `0`
   - **Refresh**: Call `InternetSetOption`.
   - **Auth**: Execute `cmdkey /delete:{ip}` (Optional clean up).

### B. System Refresh
To ensure changes apply immediately without reboot/restart:
```python
import ctypes
from ctypes import wintypes

# ... definitions ...
internet_set_option = ctypes.windll.wininet.InternetSetOptionW
internet_set_option(0, 39, 0, 0) # INTERNET_OPTION_SETTINGS_CHANGED
internet_set_option(0, 37, 0, 0) # INTERNET_OPTION_REFRESH
```

### C. Safety
- `atexit` handler to warn user if closing while connected?
- Or simpler: Just warn on close event if status is 'Connected'.

## 5. Implementation Steps
1. **Setup**: Initialize `customtkinter` app structure.
2. **Logic**: Implement `ProxyManager` class with methods `enable_proxy` and `disable_proxy`.
3. **UI**: Build layout and bind buttons to Logic.
4. **Validation**: Add checks for valid IP/Port.
5. **Testing**: Verify registry changes and network connectivity.
6. **Build**: Generate `spec` file and build EXE.

## 6. Artifacts
- `proxy_app.py`: Main source.
- `requirements.txt`: Dependencies.
- `build.bat`: Build command.
