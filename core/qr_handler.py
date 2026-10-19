#!/usr/bin/env python3
"""
Gerenciador de QR Codes para compartilhamento seguro de prontuarios medicos
Beta 2026-10-19
"""

import qrcode
import hashlib
import json
import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path


def generate_token(prontuario_id, patient_name=None, expires_hours=24):
    """
    Gera um token seguro para compartilhamento
    NAO contem PHI - apenas um ID hash
    Token URL-safe com alta entropia (secrets.token_urlsafe)
    """
    timestamp = datetime.now().isoformat()
    raw_data = f"{prontuario_id}:{timestamp}:{secrets.token_urlsafe(16)}"
    token_hash = hashlib.sha256(raw_data.encode()).hexdigest()[:32]
    return token_hash


def generate_qr_code(token, output_path=None):
    """Gera um QR Code com o token (formato wpm:token)"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"wpm:{token}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    if output_path:
        img.save(output_path)
        return output_path
    return img


def validate_token(token, tokens_dir):
    """Valida se um token existe e nao expirou"""
    token_file = Path(tokens_dir) / f"{token}.json"
    if not token_file.exists():
        return None
    
    with open(token_file, 'r') as f:
        token_data = json.load(f)
    
    expires = datetime.fromisoformat(token_data["expires"])
    if datetime.now() > expires:
        return None
    
    return token_data


def save_token_data(token_data, tokens_dir):
    """Salva dados do token"""
    token_file = Path(tokens_dir) / f"{token_data['token']}.json"
    with open(token_file, 'w') as f:
        json.dump(token_data, f)


if __name__ == "__main__":
    # Teste basico
    test_token = generate_token("prontuario_teste_001", "Joao Silva")
    print(f"Token gerado: {test_token}")
    
    qr_path = "/c/Users/User/Downloads/word-para-medicos/data/test_qr.png"
    generate_qr_code(test_token, qr_path)
    print(f"QR Code salvo em: {qr_path}")