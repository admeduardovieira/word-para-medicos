#!/usr/bin/env python3
"""
Word para Médicos - Launcher
Detecta automaticamente se tkinter está disponível e inicia a interface apropriada
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

def show_menu():
    """Mostra menu interativo para usuário"""
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    
    print("""
╔══════════════════════════════════════════════╗
║        WORD PARA MÉDICOS v1.0                ║
║      Prontuários Médicos em DOCX               ║
╚══════════════════════════════════════════════╝

[1] Novo Prontuário
[2] Abrir Prontuário
[3] Compartilhar via QR Code
[4] Ler QR Code
[5] Sair

Digite sua opção: """, end='', flush=True)

def main():
    app_dir = Path(__file__).parent
    
    if has_tkinter():
        # Iniciar interface gráfica
        try:
            from app import WordParaMedicosApp
            import tkinter as tk
            root = tk.Tk()
            app = WordParaMedicosApp(root)
            root.mainloop()
        except Exception as e:
            print(f"Erro ao iniciar GUI: {e}")
            sys.exit(1)
    else:
        # Interface CLI
        if len(sys.argv) > 1:
            # Processar argumentos de linha de comando
            from cli import main as cli_main
            cli_main()
        else:
            print("Word para Medicos - CLI Mode")
            print("=" * 40)
            print()
            print("Comandos disponiveis:")
            print("  --new --patient \"Nome\" [--doctor \"Dr.X\"] [--qr]")
            print("  --scan arquivo.png")
            print()
            print("Exemplo:")
            print("  WordParaMedicos.exe --new --patient \"Joao Silva\" --qr")
            print()
            input("Pressione ENTER para sair...")

if __name__ == "__main__":
    main()