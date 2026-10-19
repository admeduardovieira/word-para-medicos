#!/usr/bin/env python3
"""
Gerenciamento de caminhos de dados para Word para Médicos

Prioriza %LOCALAPPDATA%/WordParaMedicos/ no Windows
Funciona em modo source (python script) e frozen (PyInstaller onefile)
"""

import os
import sys
from pathlib import Path


def get_data_dir():
    """
    Retorna diretório persistente de dados do aplicativo.
    Usa LOCALAPPDATA no Windows, ~/.local/share em Linux/macOS.
    Nunca grava em sys._MEIPASS (diretório temporário do PyInstaller).
    """
    if hasattr(sys, '_MEIPASS'):
        # Executável PyInstaller - não use _MEIPASS para dados mutáveis!
        pass

    if sys.platform == 'win32':
        base = os.environ.get('LOCALAPPDATA') or os.environ.get('APPDATA')
        if base:
            return Path(base) / "WordParaMedicos"
        # Fallback se LOCALAPPDATA não definido
        return Path.home() / "AppData" / "Local" / "WordParaMedicos"

    # Linux/macOS
    return Path.home() / ".local" / "share" / "WordParaMedicos"


def get_app_dir():
    """Diretório onde o executável/script está instalado"""
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def ensure_dirs():
    """Cria necessários subdiretórios de dados"""
    data_dir = get_data_dir()
    subdirs = ['patients', 'tokens', 'exports', 'backups', 'logs']
    for sub in subdirs:
        (data_dir / sub).mkdir(parents=True, exist_ok=True)
    return data_dir


# Singleton: inicializa diretórios una vez
DATA_DIR = ensure_dirs()
APP_DIR = get_app_dir()