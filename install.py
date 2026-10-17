#!/usr/bin/env python3
"""
Instalador simples para Word para Médicos
Instala dependências e cria o executável
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def check_python():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ necessário")
        return False
    print(f"✓ Python {sys.version.split()[0]} detectado")
    return True

def install_dependencies():
    """Instala dependências necessárias"""
    packages = [
        'python-docx',
        'qrcode[pil]',
        'pyzbar',
        'pillow',
        'pyinstaller'
    ]
    
    for package in packages:
        print(f"  Instalando {package}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                     check=False, capture_output=True)
    
    print("✓ Dependências instaladas")
    return True

def build_executable():
    """Cria executável com PyInstaller"""
    app_dir = Path(__file__).parent
    cli_path = app_dir / "cli.py"
    
    if not cli_path.exists():
        print("✗ cli.py não encontrado")
        return False
    
    print("  Criando executável com PyInstaller...")
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name', 'WordParaMedicos',
        '--add-data', f'{app_dir}/data;data',
        '--hidden-import', 'docx',
        '--hidden-import', 'qrcode',
        '--hidden-import', 'pyzbar',
        '--hidden-import', 'PIL',
        str(cli_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Executável criado em dist/WordParaMedicos.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao criar executável: {e.stderr}")
        return False

def main():
    print("=" * 50)
    print("Instalador Word para Médicos")
    print("=" * 50)
    
    if not check_python():
        return 1
    
    if not install_dependencies():
        return 1
    
    if not build_executable():
        return 1
    
    print("\n=== Instalação concluída com sucesso! ===")
    print("\nPara iniciar a aplicação:")
    print("  dist/WordParaMedicos.exe --new --patient \"Nome\" --qr")
    return 0

if __name__ == "__main__":
    sys.exit(main())