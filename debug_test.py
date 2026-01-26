import sys
print("Debug script started")
print(f"Python version: {sys.version}")
try:
    import tkinter
    print("Tkinter is available")
except ImportError:
    print("Tkinter is NOT available")

print("Debug script finished")
