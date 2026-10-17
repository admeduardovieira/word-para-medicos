#!/usr/bin/env python3
"""
CLI para Word para Médicos - versão alternativa quando tkinter não disponível
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent))

from core.prontuario import ProntuarioMedico
from core.qr_handler import QRTokenManager


def main():
    parser = argparse.ArgumentParser(description="Word para Médicos - CLI")
    parser.add_argument('--new', action='store_true', help='Criar novo prontuório')
    parser.add_argument('--patient', '-p', help='Nome do paciente')
    parser.add_argument('--doctor', '-d', default='Dr. Eduardo Vieira', help='Nome do médico')
    parser.add_argument('--output', '-o', help='Arquivo de saída (.docx)')
    parser.add_argument('--qr', action='store_true', help='Gerar QR code para compartilhamento')
    parser.add_argument('--scan', help='Ler QR code de arquivo')
    
    args = parser.parse_args()
    
    app_dir = Path(__file__).parent
    data_dir = app_dir / "data"
    patients_dir = data_dir / "patients"
    patients_dir.mkdir(parents=True, exist_ok=True)
    
    qr_manager = QRTokenManager(str(data_dir))
    
    if args.new or not any([args.new, args.scan]):
        patient_name = args.patient or "Paciente Sem Nome"
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        prontuario = ProntuarioMedico()
        prontuario.add_header(patient_name, now, args.doctor)
        prontuario.add_anamnese(
            "[Queixa principal]",
            "[Histórico clínico]",
            "[Exame físico]"
        )
        prontuario.add_diagnostico("[Diagnóstico]")
        prontuario.add_prescricao("[Prescrição]")
        prontuario.add_evolucao("[Evolução]")
        
        if args.output:
            filepath = args.output
        else:
            safe_name = "".join(c for c in patient_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filepath = str(patients_dir / f"{safe_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx")
        
        prontuario.save(filepath)
        print(f"✓ Prontuário criado: {filepath}")
        
        if args.qr:
            token = qr_manager.generate_token(Path(filepath).name, patient_name)
            qr_path = str(Path(filepath).parent / f"qr_{token}.png")
            qr_manager.generate_qr_code(token, qr_path)
            print(f"✓ QR Code gerado: {qr_path}")
            print(f"  Token: {token}")
    
    elif args.scan:
        try:
            from pyzbar.pyzbar import decode
            from PIL import Image
            
            img = Image.open(args.scan)
            decoded = decode(img)
            
            if decoded:
                data = decoded[0].data.decode('utf-8')
                if data.startswith("wpm:"):
                    token = data[3:]
                    token_data = qr_manager.validate_token(token)
                    
                    if token_data:
                        prontuario_id = token_data["prontuario_id"]
                        prontuario_path = patients_dir / prontuario_id
                        
                        if prontuario_path.exists():
                            print(f"✓ Prontuário acessado via QR Code: {prontuario_path}")
                            from docx import Document
                            doc = Document(str(prontuario_path))
                            for p in doc.paragraphs:
                                if p.text:
                                    print(f"  {p.text}")
                        else:
                            print(f"✗ Prontuário não encontrado: {prontuario_id}")
                    else:
                        print("✗ Token inválido ou expirado")
                else:
                    print(f"Dados do QR: {data}")
            else:
                print("✗ Nenhum código QR encontrado")
                
        except ImportError:
            print("✗ Bibliotecas de leitura de QR não instaladas (pyzbar)")
        except Exception as e:
            print(f"✗ Erro: {e}")
    
    print("\nUso:")
    print("  python3 cli.py --new --patient \"João Silva\" --qr")
    print("  python3 cli.py --scan qr_code.png")


if __name__ == "__main__":
    main()