#!/usr/bin/env python3

import tkinter as tk
import os

# Tentar criar uma instância mínima
try:
    root = tk.Tk()
    root.destroy()
    print("tkinter disponível.")
except ImportError:
    print("tkinter não disponível.")

# Verificar dependências
try:
    import docx
    print(f"python-docx versão: {docx.__version__}")
except ImportError:
    print("python-docx não instalado.")

try:
    import qrcode
    print(f"qrcode versão: {qrcode.__version__}")
except ImportError:
    print("qrcode não instalado.")

try:
    from pyzbar.pyzbar import decode
    print("pyzbar disponível.")
except ImportError:
    print("pyzbar não instalado.")

from PIL import Image
print("Pillow disponível.")