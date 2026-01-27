import customtkinter as ctk
print("Starting ASB SimpleProxy...")
import logging
import sys

# Configure logging to use local directory
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("proxy_app.log", mode='a', encoding='utf-8')
    ]
)

# Mapping of Russian letters to English for keyboard layout handling
RUSSIAN_TO_ENGLISH = {
    'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']',
    'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';', 'э': "'",
    'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.',
    'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T', 'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P', 'Х': '[', 'Ъ': ']',
    'Ф': 'A', 'Ы': 'S', 'В': 'D', 'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K', 'Д': 'L', 'Ж': ';', 'Э': "'",
    'Я': 'Z', 'Ч': 'X', 'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M', 'Б': ',', 'Ю': '.'
}

def transliterate_layout(text):
    """Convert Russian letters to English, preserving digits and special chars."""
    result = []
    for char in text:
        result.append(RUSSIAN_TO_ENGLISH.get(char, char))
    return ''.join(result)

# Language translations
LANGUAGES = {
    'en': {
        'app_title': 'ASB SimpleProxy - Proxy Manager',
        'ip_address': 'IP Address',
        'port': 'Port',
        'username': 'Username',
        'password': 'Password',
        'proxy_type': 'Proxy Type',
        'connect': 'Connect',
        'disconnect': 'Disconnect',
        'status_disconnected': 'Status: Disconnected',
        'status_connecting': 'Status: Connecting...',
        'status_connected': 'Status: Connected',
        'error_invalid_ip': 'Invalid IP Address format.',
        'error_invalid_port': 'Port must be a number between 1 and 65535.',
        'error_auth': 'Authentication Error',
        'error_auth_msg': 'Invalid username or password for proxy connection.',
        'registry_error': 'Registry Error',
        'btn_lang': 'RU',
        'settings_saved': 'Settings saved',
    },
    'ru': {
        'app_title': 'ASB SimpleProxy - Менеджер прокси',
        'ip_address': 'IP адрес',
        'port': 'Порт',
        'username': 'Логин',
        'password': 'Пароль',
        'proxy_type': 'Тип прокси',
        'connect': 'Подключить',
        'disconnect': 'Отключить',
        'status_disconnected': 'Статус: Отключено',
        'status_connecting': 'Статус: Подключение...',
        'status_connected': 'Статус: Подключено',
        'error_invalid_ip': 'Неверный формат IP адреса.',
        'error_invalid_port': 'Порт должен быть числом от 1 до 65535.',
        'error_auth': 'Ошибка аутентификации',
        'error_auth_msg': 'Неверный логин или пароль для подключения к прокси.',
        'registry_error': 'Ошибка реестра',
        'btn_lang': 'EN',
        'settings_saved': 'Настройки сохранены',
    }
}

# Current language
current_language = 'en'

logging.info("Initializing application...")

import customtkinter as ctk
logging.info("Imported customtkinter")
import winreg
logging.info("Imported winreg")
import ctypes
import subprocess
import socket
import threading
import atexit
import json
import os
from tkinter import messagebox
logging.info("Imported all dependencies")

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
logging.info("CTk configuration set")

# Simple encryption for storing sensitive data
def encrypt_data(data, key="SimpleProxyConnect"):
    """Simple XOR encryption for storing sensitive data."""
    import base64
    encrypted_chars = []
    for i, char in enumerate(data):
        key_char = key[i % len(key)]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        encrypted_chars.append(encrypted_char)
    return base64.b64encode(''.join(encrypted_chars).encode()).decode()

def decrypt_data(encrypted_data, key="SimpleProxyConnect"):
    """Simple XOR decryption for retrieving sensitive data."""
    import base64
    try:
        decrypted_chars = []
        decoded_data = base64.b64decode(encrypted_data.encode()).decode()
        for i, char in enumerate(decoded_data):
            key_char = key[i % len(key)]
            decrypted_char = chr(ord(char) ^ ord(key_char))
            decrypted_chars.append(decrypted_char)
        return ''.join(decrypted_chars)
    except:
        return ""  # Return empty string if decryption fails

def save_settings(settings):
    """Save settings to a file."""
    try:
        encrypted_settings = {}
        for key, value in settings.items():
            if key in ['username', 'password']:
                encrypted_settings[key] = encrypt_data(value)
            else:
                encrypted_settings[key] = value
        
        with open('settings.json', 'w') as f:
            json.dump(encrypted_settings, f)
    except Exception as e:
        print(f"Error saving settings: {e}")

def load_settings():
    """Load settings from a file."""
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                encrypted_settings = json.load(f)
            
            settings = {}
            for key, value in encrypted_settings.items():
                if key in ['username', 'password']:
                    settings[key] = decrypt_data(value)
                else:
                    settings[key] = value
            return settings
        else:
            return {}
    except Exception as e:
        print(f"Error loading settings: {e}")
        return {}

class LocalProxyTunnel:
    """A local proxy tunnel that forwards connections to remote authenticated proxy."""
    
    def __init__(self, remote_ip, remote_port, username, password, local_port=8081):
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.username = username
        self.password = password
        self.local_port = local_port
        self.running = False
        self.thread = None
        self.shutdown_event = threading.Event()
        self.auth_error = None  # Store authentication error
        
    def start(self):
        """Start the local proxy tunnel."""
        self.running = True
        self.shutdown_event.clear()
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the local proxy tunnel."""
        self.running = False
        if self.shutdown_event:
            self.shutdown_event.set()
        if self.thread:
            self.thread.join(timeout=2)
    
    def _run_server(self):
        """Run the local proxy server."""
        import socket
        import select
        import base64
        
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('127.0.0.1', self.local_port))
            server_socket.listen(5)
            server_socket.settimeout(1)
            
            print(f"Local proxy tunnel listening on 127.0.0.1:{self.local_port}")
            
            while self.running and not self.shutdown_event.is_set():
                try:
                    ready, _, _ = select.select([server_socket], [], [], 1)
                    if not ready:
                        continue
                        
                    client_socket, addr = server_socket.accept()
                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client, 
                        args=(client_socket,), 
                        daemon=True
                    )
                    client_thread.start()
                except socket.timeout:
                    continue
                except OSError:
                    if self.running and not self.shutdown_event.is_set():  # Only log if we're supposed to be running
                        print("Error accepting connections")
                    break
                except Exception as e:
                    print(f"Unexpected error in server loop: {e}")
                    break
                    
            server_socket.close()
            
        except Exception as e:
            print(f"Error starting local proxy tunnel: {e}")
    
    def _handle_client(self, client_socket):
        """Handle a client connection with proper HTTP proxy protocol."""
        remote_socket = None
        try:
            # Receive initial request from client
            client_socket.settimeout(10)  # 10 seconds timeout for initial request
            request = client_socket.recv(4096)
            
            # Parse the HTTP request to extract method and destination
            request_str = request.decode('utf-8', errors='ignore')
            lines = request_str.split('\n')
            if lines:
                first_line = lines[0].strip()
                parts = first_line.split()
                
                if len(parts) >= 3 and parts[0] == 'CONNECT':
                    # This is an HTTPS CONNECT request
                    host_port = parts[1]
                    print(f"Handling CONNECT request to {host_port}")
                    
                    # Establish connection to remote proxy with authentication
                    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote_socket.connect((self.remote_ip, int(self.remote_port)))
                    
                    # Send CONNECT request to remote proxy with authentication
                    # Construct proxy authorization header
                    import base64
                    credentials = f"{self.username}:{self.password}"
                    encoded_credentials = base64.b64encode(credentials.encode()).decode()
                    
                    connect_request = (
                        f"CONNECT {host_port} HTTP/1.1\r\n"
                        f"Host: {host_port}\r\n"
                        f"Proxy-Authorization: Basic {encoded_credentials}\r\n"
                        f"Connection: Keep-Alive\r\n"
                        f"\r\n"
                    )
                    
                    remote_socket.send(connect_request.encode())
                    
                    # Receive response from remote proxy
                    remote_socket.settimeout(10)
                    response = remote_socket.recv(4096)
                    response_str = response.decode('utf-8', errors='ignore')
                    
                    # Check if connection was successful (200 OK)
                    if '200' in response_str or 'connection established' in response_str.lower():
                        # Send success response back to client
                        client_socket.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")
                        
                        # Now forward data bidirectionally
                        self._forward_data(client_socket, remote_socket)
                    elif '407' in response_str or 'proxy authentication required' in response_str.lower():
                        # Authentication failed
                        print(f"Authentication failed: {response_str}")
                        self.auth_error = "Invalid username or password"
                        client_socket.send(b"HTTP/1.1 407 Proxy Authentication Required\r\n\r\n")
                    else:
                        print(f"Failed to establish connection through proxy: {response_str}")
                        client_socket.send(b"HTTP/1.1 502 Proxy Connection Failed\r\n\r\n")
                        
                else:
                    # For other HTTP requests, we'll forward them with authentication
                    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote_socket.connect((self.remote_ip, int(self.remote_port)))
                    
                    # Add proxy authorization to the request
                    import base64
                    credentials = f"{self.username}:{self.password}"
                    encoded_credentials = base64.b64encode(credentials.encode()).decode()
                    
                    # Modify the request to include proxy authorization
                    if 'Proxy-Authorization:' not in request_str:
                        # Find where headers end
                        header_end = request_str.find('\r\n\r\n')
                        if header_end != -1:
                            headers = request_str[:header_end]
                            body = request_str[header_end:]
                            
                            # Add proxy authorization header
                            new_request = (
                                headers + 
                                f"\r\nProxy-Authorization: Basic {encoded_credentials}" +
                                body
                            )
                        else:
                            # If no body, just append the header
                            new_request = request_str.rstrip() + f"\r\nProxy-Authorization: Basic {encoded_credentials}\r\n\r\n"
                        
                        remote_socket.send(new_request.encode())
                    else:
                        remote_socket.send(request)
                    
                    # Forward response back to client
                    response = remote_socket.recv(4096)
                    client_socket.send(response)
                    
                    # Continue forwarding any remaining data
                    self._forward_data(client_socket, remote_socket)
            
        except Exception as e:
            print(f"Error handling client connection: {e}")
            try:
                client_socket.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
            except:
                pass
        finally:
            if client_socket:
                client_socket.close()
            if remote_socket:
                remote_socket.close()
    
    def _forward_data(self, client_socket, remote_socket):
        """Forward data between client and remote proxy."""
        import select
        try:
            while self.running and not self.shutdown_event.is_set():
                ready, _, error = select.select([client_socket, remote_socket], [], [client_socket, remote_socket], 1)
                
                if error or self.shutdown_event.is_set():
                    break
                
                if client_socket in ready:
                    data = client_socket.recv(4096)
                    if not data or self.shutdown_event.is_set():
                        break
                    remote_socket.send(data)
                
                if remote_socket in ready:
                    data = remote_socket.recv(4096)
                    if not data or self.shutdown_event.is_set():
                        break
                    client_socket.send(data)
        except Exception as e:
            print(f"Error forwarding data: {e}")

class ProxyManager:
    """Handles Windows Registry and System settings for Proxy configuration."""
    
    REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

    @staticmethod
    def set_registry_proxy(ip, port, enabled=True, user=None, password=None):
        """Sets the proxy in the Windows Registry."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, ProxyManager.REG_PATH, 0, winreg.KEY_WRITE)
            
            if enabled:
                if user and password:
                    # Include credentials in proxy server string (format: protocol://user:pass@host:port)
                    # However, Windows registry doesn't typically support embedded credentials in proxy URLs
                    # So we'll set the basic proxy server and store credentials separately
                    proxy_server = f"{ip}:{port}"
                else:
                    proxy_server = f"{ip}:{port}"
                    
                winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy_server)
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                # Ensure local addresses are bypassed
                winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, "<local>")
            else:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)

            winreg.CloseKey(key)
            return True, "Registry updated successfully."
        except Exception as e:
            return False, f"Registry Error: {str(e)}"

    @staticmethod
    def refresh_system():
        """Notifies the system that internet settings have changed."""
        try:
            # INTERNET_OPTION_SETTINGS_CHANGED = 39
            # INTERNET_OPTION_REFRESH = 37
            internet_set_option = ctypes.windll.wininet.InternetSetOptionW
            internet_set_option(0, 39, 0, 0)
            internet_set_option(0, 37, 0, 0)
            return True
        except Exception as e:
            return False

    @staticmethod
    def set_credentials(ip, user, password):
        """Adds credentials to Windows Credential Manager using cmdkey."""
        try:
            # Using cmdkey to store credentials. 
            # Note: Browsers might still prompt, but this covers system services.
            # Targeted at the IP:Port or just IP
            target = f"{ip}"
            subprocess.run(f"cmdkey /add:{target} /user:{user} /pass:{password}", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False

    @staticmethod
    def clear_credentials(ip):
        try:
            target = f"{ip}"
            subprocess.run(f"cmdkey /delete:{target}", shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Language
        self.language = current_language
        
        self.title(LANGUAGES[self.language]['app_title'])
        self.geometry("400x550")
        self.resizable(False, False)
        
        # Grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(12, weight=1) # Spacer

        # Language button
        self.btn_lang = ctk.CTkButton(self, text=LANGUAGES[self.language]['btn_lang'], 
                                       width=40, height=30, command=self.toggle_language)
        self.btn_lang.grid(row=0, column=0, padx=(140, 0), pady=(20, 0), sticky="e")
        
        # Header
        self.lbl_title = ctk.CTkLabel(self, text="ASB SimpleProxy", font=("Roboto Medium", 20))
        self.lbl_title.grid(row=0, column=0, pady=(20, 0))

        # Inputs
        self.entry_ip = self.create_input(LANGUAGES[self.language]['ip_address'], "", 1)
        self.entry_port = self.create_input(LANGUAGES[self.language]['port'], "", 2)
        self.entry_user = self.create_input(LANGUAGES[self.language]['username'], "", 3)
        self.entry_pass = self.create_input(LANGUAGES[self.language]['password'], "", 4, show="*")

        # Proxy Type (Dropdown)
        self.lbl_type = ctk.CTkLabel(self, text=LANGUAGES[self.language]['proxy_type'], anchor="w")
        self.lbl_type.grid(row=9, column=0, padx=30, pady=(5, 0), sticky="w")
        self.opt_type = ctk.CTkOptionMenu(self, values=["HTTPS", "HTTP"])
        self.opt_type.grid(row=10, column=0, padx=30, pady=(0, 20), sticky="ew")

        # Buttons Frame
        self.frm_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frm_buttons.grid(row=11, column=0, padx=30, pady=20, sticky="ew")
        self.frm_buttons.grid_columnconfigure((0, 1), weight=1)

        self.btn_connect = ctk.CTkButton(self.frm_buttons, text=LANGUAGES[self.language]['connect'], fg_color="#2CC985", hover_color="#229B65", height=50, command=self.on_connect)
        self.btn_connect.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.btn_disconnect = ctk.CTkButton(self.frm_buttons, text=LANGUAGES[self.language]['disconnect'], fg_color="#E74C3C", hover_color="#C0392B", height=50, command=self.on_disconnect)
        self.btn_disconnect.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # Status Bar
        self.lbl_status = ctk.CTkLabel(self, text=LANGUAGES[self.language]['status_disconnected'], fg_color="#222", corner_radius=0, anchor="w", padx=10)
        self.lbl_status.grid(row=12, column=0, sticky="ew")
        
        # Load saved settings
        saved_settings = load_settings()
        
        # Initial State
        if saved_settings.get('ip'):
            self.entry_ip.insert(0, saved_settings.get('ip', ""))
        if saved_settings.get('port'):
            self.entry_port.insert(0, saved_settings.get('port', ""))
        if saved_settings.get('username'):
            self.entry_user.insert(0, saved_settings.get('username', ""))
        if saved_settings.get('password'):
            self.entry_pass.insert(0, saved_settings.get('password', ""))
        
        # Local proxy tunnel instance
        self.local_tunnel = None
        
        # Configure window closing behavior
        # Handler is set in if __name__ == "__main__" block
        
        # Enable window maximizing
        self.state('normal')
        
        # Cleanup on exit
        # Removed atexit registration to prevent blocking during forced exit

    def create_input(self, label_text, placeholder, row, show=None):
        label = ctk.CTkLabel(self, text=label_text, anchor="w")
        label.grid(row=(row-1)*2 + 1, column=0, padx=30, pady=(5, 0), sticky="w")
        entry = ctk.CTkEntry(self, placeholder_text=placeholder, show=show)
        entry.grid(row=(row-1)*2 + 2, column=0, padx=30, pady=(0, 10), sticky="ew")
        
        # Add keyboard layout handling for IP and Port fields
        # Check for both English and Russian labels
        ip_labels = ["IP Address", "IP адрес"]
        port_labels = ["Port", "Порт"]
        
        if label_text in ip_labels or label_text in port_labels:
            # Add keyboard shortcuts for copy/paste that work in any layout
            try:
                def do_copy():
                    try:
                        entry.event_generate('<<Copy>>')
                    except Exception as e:
                        print(f"Copy error: {e}")
                
                def do_paste():
                    # Get clipboard and transliterate if needed
                    try:
                        clipboard = self.clipboard_get()
                        # For IP and Port fields, we don't need transliteration
                        # since we're dealing with numbers and dots
                        # But we'll keep it for compatibility with other input types
                        transliterated = transliterate_layout(clipboard)
                        # Delete selected text if any
                        try:
                            entry.delete(entry.selection_get())
                        except:
                            pass
                        # Insert transliterated text
                        entry.insert("insert", transliterated)
                    except Exception as e:
                        print(f"Paste error: {e}")
                
                # Multiple bindings to support different keyboard layouts
                # English layout bindings
                entry.bind('<Control-c>', lambda e: do_copy())
                entry.bind('<Control-C>', lambda e: do_copy())
                entry.bind('<Control-v>', lambda e: do_paste())
                entry.bind('<Control-V>', lambda e: do_paste())
                
                # Russian layout bindings (where 'c' is 'с' and 'v' is 'м')
                entry.bind('<Control-с>', lambda e: do_copy())
                entry.bind('<Control-С>', lambda e: do_copy())
                entry.bind('<Control-м>', lambda e: do_paste())
                entry.bind('<Control-М>', lambda e: do_paste())
                
                # Also keep physical keycode bindings as fallback
                entry.bind('<Control-KeyPress-67>', lambda e: do_copy())  # Ctrl+C
                entry.bind('<Control-KeyPress-86>', lambda e: do_paste())  # Ctrl+V
            except Exception as e:
                print(f"Binding error: {e}")
            
            # Create context menu with paste option that handles keyboard layout
            context_menu = ctk.CTkFrame(self, fg_color="#333333")
            
            def do_paste_menu():
                # Get clipboard and transliterate if needed
                try:
                    clipboard = self.clipboard_get()
                    transliterated = transliterate_layout(clipboard)
                    # Delete selected text if any
                    try:
                        entry.delete(entry.selection_get())
                    except:
                        pass
                    # Insert transliterated text
                    entry.insert("insert", transliterated)
                except:
                    pass
            
            # Create paste button with proper translation
            paste_text = "Paste" if self.language == 'en' else "Вставить"
            paste_btn = ctk.CTkButton(context_menu, text=paste_text, width=100, height=30, 
                                       command=do_paste_menu)
            paste_btn.pack(padx=5, pady=5)
            
            def show_context_menu(event):
                try:
                    # Update paste button text based on current language
                    paste_btn.configure(text="Paste" if self.language == 'en' else "Вставить")
                    context_menu.place(x=event.x_root - self.winfo_rootx(), 
                                      y=event.y_root - self.winfo_rooty())
                    entry.focus_set()
                    self.after(3000, lambda: context_menu.place_forget())
                except:
                    pass
            
            entry.bind("<Button-3>", show_context_menu)
        
        def _handle_paste(entry_widget):
            try:
                clipboard = self.clipboard_get()
                transliterated = transliterate_layout(clipboard)
                try:
                    entry_widget.delete(entry_widget.selection_get())
                except:
                    pass
                entry_widget.insert("insert", transliterated)
            except:
                pass
        
        return entry

    def validate_inputs(self):
        ip = self.entry_ip.get().strip()
        port = self.entry_port.get().strip()
        
        try:
            socket.inet_aton(ip)
        except socket.error:
            messagebox.showerror(LANGUAGES[self.language]['registry_error'], LANGUAGES[self.language]['error_invalid_ip'])
            return False
            
        if not port.isdigit() or not (1 <= int(port) <= 65535):
            messagebox.showerror(LANGUAGES[self.language]['registry_error'], LANGUAGES[self.language]['error_invalid_port'])
            return False
            
        return True

    def on_connect(self):
        # First, disconnect any existing connection
        self.on_disconnect()
        
        if not self.validate_inputs():
            return

        ip = self.entry_ip.get().strip()
        port = self.entry_port.get().strip()
        proxy_type = self.opt_type.get().lower()  # Get the selected proxy type
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        
        # Save settings for future use
        settings_to_save = {
            'ip': ip,
            'port': port,
            'username': user,
            'password': password
        }
        save_settings(settings_to_save)
        
        # If credentials are provided, use local proxy tunnel
        if user and password:
            # Start local proxy tunnel
            self.local_tunnel = LocalProxyTunnel(ip, port, user, password)
            self.local_tunnel.start()
            
            # Set Windows proxy to local tunnel
            success, msg = ProxyManager.set_registry_proxy('127.0.0.1', str(self.local_tunnel.local_port), enabled=True)
            
            # Update status to connecting
            self.update_status(f"{LANGUAGES[self.language]['status_connecting']} {proxy_type.upper()} {ip}:{port}...", connected=False)
            
            # Start periodic check for authentication errors
            self._check_auth_error()
        else:
            # Set Windows proxy directly to remote server
            success, msg = ProxyManager.set_registry_proxy(ip, port, enabled=True, user=user, password=password)
        
        if not success:
            messagebox.showerror(LANGUAGES[self.language]['registry_error'], msg)
            if self.local_tunnel:
                self.local_tunnel.stop()
                self.local_tunnel = None
            return

        # Store Credentials (if provided) - additional security measure
        if user and password:
            ProxyManager.set_credentials(ip, user, password)

        # Refresh System
        ProxyManager.refresh_system()

        if user and password:
            self.update_status(f"{LANGUAGES[self.language]['status_connected']} via local tunnel to {proxy_type.upper()} {ip}:{port}", connected=True)
        else:
            self.update_status(f"{LANGUAGES[self.language]['status_connected']} to {proxy_type.upper()} {ip}:{port}", connected=True)

    def _check_auth_error(self):
        """Periodically check for authentication errors."""
        if self.local_tunnel and self.local_tunnel.auth_error:
            # Authentication failed
            self.local_tunnel.stop()
            self.local_tunnel = None
            
            # Disconnect proxy settings
            ProxyManager.set_registry_proxy("", "", enabled=False)
            ProxyManager.refresh_system()
            
            # Update status
            self.update_status(f"Error: {LANGUAGES[self.language]['error_auth_msg']}", connected=False)
            messagebox.showerror(LANGUAGES[self.language]['error_auth'], LANGUAGES[self.language]['error_auth_msg'])
        elif self.local_tunnel:
            # Continue checking if tunnel is still running
            self.after(1000, self._check_auth_error)

    def on_disconnect(self):
        # Stop local tunnel if running
        if self.local_tunnel:
            self.local_tunnel.stop()
            self.local_tunnel = None

        # 1. Update Registry
        ProxyManager.set_registry_proxy("", "", enabled=False)

        # 2. Clear Credentials (optional, but good practice)
        ip = self.entry_ip.get().strip()
        if ip:
            ProxyManager.clear_credentials(ip)

        # 3. Refresh System
        ProxyManager.refresh_system()

        self.update_status(LANGUAGES[self.language]['status_disconnected'], connected=False)

    def toggle_language(self):
        """Toggle between English and Russian languages."""
        self.language = 'ru' if self.language == 'en' else 'en'
        self.recreate_ui()
    
    def recreate_ui(self):
        """Recreate all UI elements with current language."""
        # Save current values
        ip_value = self.entry_ip.get()
        port_value = self.entry_port.get()
        user_value = self.entry_user.get()
        pass_value = self.entry_pass.get()
        proxy_type = self.opt_type.get()
        
        # Get current connection status
        is_connected = self.local_tunnel is not None
        
        # Clear and recreate all UI elements
        for widget in self.winfo_children():
            widget.destroy()
        
        # Reinitialize grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(12, weight=1)
        
        # Header
        self.lbl_title = ctk.CTkLabel(self, text="ASB SimpleProxy", font=("Roboto Medium", 20))
        self.lbl_title.grid(row=0, column=0, pady=(20, 0))
        
        # Language button with inverted colors
        is_russian = self.language == 'ru'
        btn_fg = "#1A1A1A" if is_russian else "#3B8ED0"  # Inverted colors
        btn_hover = "#2D2D2D" if is_russian else "#36719F"
        self.btn_lang = ctk.CTkButton(self, text=LANGUAGES[self.language]['btn_lang'], 
                                       width=40, height=30, command=self.toggle_language,
                                       fg_color=btn_fg, hover_color=btn_hover)
        self.btn_lang.grid(row=0, column=0, padx=(140, 0), pady=(20, 0), sticky="e")
        
        # Inputs with new language
        self.entry_ip = self.create_input(LANGUAGES[self.language]['ip_address'], "", 1)
        self.entry_port = self.create_input(LANGUAGES[self.language]['port'], "", 2)
        self.entry_user = self.create_input(LANGUAGES[self.language]['username'], "", 3)
        self.entry_pass = self.create_input(LANGUAGES[self.language]['password'], "", 4, show="*")
        
        # Restore values
        if ip_value:
            self.entry_ip.insert(0, ip_value)
        if port_value:
            self.entry_port.insert(0, port_value)
        if user_value:
            self.entry_user.insert(0, user_value)
        if pass_value:
            self.entry_pass.insert(0, pass_value)
        
        # Proxy Type
        self.lbl_type = ctk.CTkLabel(self, text=LANGUAGES[self.language]['proxy_type'], anchor="w")
        self.lbl_type.grid(row=9, column=0, padx=30, pady=(5, 0), sticky="w")
        self.opt_type = ctk.CTkOptionMenu(self, values=["HTTPS", "HTTP"])
        self.opt_type.set(proxy_type)
        self.opt_type.grid(row=10, column=0, padx=30, pady=(0, 20), sticky="ew")
        
        # Buttons Frame
        self.frm_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frm_buttons.grid(row=11, column=0, padx=30, pady=(10, 0), sticky="ew")
        self.frm_buttons.grid_columnconfigure((0, 1), weight=1)
        
        self.btn_connect = ctk.CTkButton(self.frm_buttons, text=LANGUAGES[self.language]['connect'], 
                                          fg_color="#2CC985", hover_color="#229B65", height=50, 
                                          command=self.on_connect)
        self.btn_connect.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        self.btn_disconnect = ctk.CTkButton(self.frm_buttons, text=LANGUAGES[self.language]['disconnect'], 
                                             fg_color="#E74C3C", hover_color="#C0392B", height=50, 
                                             command=self.on_disconnect)
        self.btn_disconnect.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        
        # Status Bar
        status_color = "#2CC985" if is_connected else "#E74C3C"
        self.lbl_status = ctk.CTkLabel(self, text=LANGUAGES[self.language]['status_disconnected'], 
                                        fg_color="#222", corner_radius=0, anchor="w", padx=10,
                                        text_color=status_color if is_connected else "#E74C3C")
        self.lbl_status.grid(row=12, column=0, sticky="ew")
        
        # Restore connection status text
        if is_connected:
            ip = self.entry_ip.get().strip()
            port = self.entry_port.get().strip()
            proxy_type_lower = self.opt_type.get().lower()
            self.lbl_status.configure(text=f"{LANGUAGES[self.language]['status_connected']} to {proxy_type_lower.upper()} {ip}:{port}")
        
        # Re-enable window
        self.state('normal')

    def update_status(self, text, connected):
        self.lbl_status.configure(text=f"Status: {text}", text_color="#2CC985" if connected else "#E74C3C")

    def on_closing(self):
        """Handle window closing event - force close with disconnect."""
        import os
        import ctypes
        import signal
        
        # 1. Stop local tunnel if running
        if self.local_tunnel:
            try:
                self.local_tunnel.stop()
                self.local_tunnel = None
            except:
                pass
        
        # 2. Update Registry - disconnect proxy
        try:
            ProxyManager.set_registry_proxy("", "", enabled=False)
            ip = self.entry_ip.get().strip()
            if ip:
                ProxyManager.clear_credentials(ip)
            ProxyManager.refresh_system()
        except:
            pass
        
        # 3. Update status
        try:
            self.lbl_status.configure(text="Status: Disconnected", text_color="#E74C3C")
        except:
            pass
        
        # 4. Force exit using TerminateProcess via ctypes for PyInstaller apps
        try:
            ctypes.windll.kernel32.TerminateProcess(-1, 0)
        except:
            pass
        
        # 5. Fallback - force exit
        os._exit(0)

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # Use on_closing for proper exit
    app.mainloop()
