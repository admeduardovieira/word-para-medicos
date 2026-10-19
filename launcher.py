#!/usr/bin/env python3
"""
Word para Médicos - Launcher
Beta 2026-10-19
"""

import os
import sys
from pathlib import Path

# Adicionar diretório ao path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))


def has_tkinter():
    """Verifica se tkinter está disponível"""
    try:
        import tkinter
        root = tkinter.Tk()
        root.destroy()
        return True
    except (ImportError, Exception):
        return False


def main():
    if has_tkinter():
        try:
            from app import WordParaMedicosApp
            import tkinter as tk
            root = tk.Tk()
            app = WordParaMedicosApp(root)
            root.protocol("WM_DELETE_WINDOW", app.on_closing)
            root.mainloop()
        except Exception as e:
            print(f"Erro ao iniciar GUI: {e}")
            sys.exit(1)
    else:
        if len(sys.argv) > 1:
            from cli import main as cli_main
            cli_main()
        else:
            print("Word para Medicos - CLI Mode")
            print("=" * 40)
            print()
            print("Comandos disponiveis:")
            print("  --new --patient \"Nome\" [--doctor \"Dr.X\"]")
            print()
            if sys.platform == 'win32':
                input("Pressione ENTER para sair...")
            else:
                sys.stdin.readline()


if __name__ == "__main__":
    main()