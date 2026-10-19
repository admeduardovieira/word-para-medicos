#!/usr/bin/env python3
"""
CLI para Word para Médicos - versão alternativa quando tkinter não disponível
Beta 2026-10-19
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Forçar UTF-8 no Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Caracteres ASCII-compatíveis para Windows
CHECK = "[OK]"
ERROR = "[ERRO]"
INFO = "[INFO]"

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent))

from core.paths import DATA_DIR
from core.prontuario import ProntuarioMedico
from core.qr_handler import QRTokenManager

PATIENTS_DIR = DATA_DIR / "patients"
PATIENTS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Word para Medicos - CLI")
    parser.add_argument('--new', action='store_true', help='Criar novo prontuario')
    parser.add_argument('--patient', '-p', help='Nome do paciente (dados ficticios)')
    parser.add_argument('--doctor', '-d', default='Dr. Eduardo Vieira', help='Nome do medico')
    parser.add_argument('--output', '-o', help='Arquivo de saida (.docx)')
    parser.add_argument('--qr', action='store_true', help='Gerar QR code temporario (LAN)')
    parser.add_argument('--scan', help='Ler QR code de arquivo')
    
    args = parser.parse_args()
    
    data_dir = DATA_DIR
    qr_manager = QRTokenManager(str(data_dir))
    
    if args.new or not any([args.scan]):
        patient_name = args.patient or "[Paciente Ficticio]"
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        prontuario = ProntuarioMedico()
        prontuario.add_header(patient_name, now, args.doctor)
        prontuario.add_anamnese("[Queixa principal]", "[Historico clinico]", "[Exame fisico]")
        prontuario.add_diagnostico("[Diagnostico]")
        prontuario.add_prescricao("[Prescricao]")
        prontuario.add_evolucao("[Evolucao]")
        
        if args.output:
            filepath = args.output
        else:
            safe_name = "".join(c for c in patient_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filepath = str(PATIENTS_DIR / f"{safe_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx")
        
        prontuario.save(filepath)
        print(f"[{CHECK}] Prontuario criado: {filepath}")
        
        if args.qr:
            print(f"\n[{INFO}] Compartilhamento via QR requer a interface grafica (app.py)")
            print(f"  Abra app.py para compartilhar via rede local com QR Code")
    elif args.scan:
        print(f"[{INFO}] Leitura de QR requer pyzbar. Use a interface grafica.")
    else:
        print(" uso:")
        print("  python3 cli.py --new --patient \"Nome do Paciente\"")
        print("  python3 cli.py --scan qr_code.png")


if __name__ == "__main__":
    main()