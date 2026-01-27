# ASB SimpleProxy

A simple and powerful Windows proxy manager application with support for HTTP/HTTPS proxies, authentication handling, and multilingual interface (English/Russian).

## Features

- Connect to HTTP/HTTPS proxies with authentication
- Automatic proxy configuration in Windows registry
- Local proxy tunnel for handling authentication
- Multilingual interface (English/Russian)
- Compact portable version available
- Status monitoring
- Automatic reconnection support

## Requirements

- Windows 10/11
- Python 3.8+
- Administrator privileges (for registry modification)

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/ASB-MSK/SimpleProxyASB.git
cd SimpleProxyASB
```

2. Install dependencies:
```bash
pip install customtkinter pyinstaller
```

3. Run the application:
```bash
python proxy_app.py
```

### Portable Version

Download the portable version from the [releases page](https://github.com/ASB-MSK/SimpleProxyASB/releases):
- Extract the ZIP file
- Run `SimpleProxyASB.exe`

## Building from Source

To create a portable version:

```bash
pyinstaller --onefile --windowed --name SimpleProxyASB proxy_app.py
```

The executable will be in the `dist/` folder.

## Usage

1. Enter the proxy IP address and port
2. (Optional) Enter username and password for authentication
3. Select proxy type (HTTP or HTTPS)
4. Click "Connect" to establish the connection
5. Click "Disconnect" to stop using the proxy

## Language

Click the "RU/EN" button in the top-right corner to switch between English and Russian languages.

## License

MIT License - see LICENSE file for details.

## Author

ASB-MSK - https://github.com/ASB-MSK
