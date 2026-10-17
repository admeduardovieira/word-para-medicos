#!/usr/bin/env python3
"""
Gerenciador de QR Codes para compartilhamento seguro de prontuários médicos
"""

import qrcode
import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class QRTokenManager:
    """Gerencia tokens seguros para compartilhamento de prontuários"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.tokens_dir = self.data_dir / "tokens"
        self.tokens_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_token(self, prontuario_id, patient_name=None, expires_hours=24):
        """
        Gera um token seguro para compartilhamento
        NÃO contém PHI - apenas um ID hash
        """
        # Criar hash do prontuário ID + timestamp
        timestamp = datetime.now().isoformat()
        raw_data = f"{prontuario_id}:{timestamp}"
        token_hash = hashlib.sha256(raw_data.encode()).hexdigest()[:32]
        
        # Criar token com metadata mínima
        token_data = {
            "token": token_hash,
            "prontuario_id": prontuario_id,
            "created": timestamp,
            "expires": (datetime.now() + timedelta(hours=expires_hours)).isoformat(),
            "patient_name_hash": hashlib.sha256(patient_name.encode()).hexdigest()[:16] if patient_name else None
        }
        
        # Salvar token localmente
        token_file = self.tokens_dir / f"{token_hash}.json"
        with open(token_file, 'w') as f:
            json.dump(token_data, f)
        
        return token_hash
    
    def generate_qr_code(self, token, output_path=None):
        """Gera um QR Code com o token"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"wpm:{token}")  # Prefixo da aplicação
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        if output_path:
            img.save(output_path)
            return output_path
        return img
    
    def validate_token(self, token):
        """Valida se um token existe e não expirou"""
        token_file = self.tokens_dir / f"{token}.json"
        if not token_file.exists():
            return None
        
        with open(token_file, 'r') as f:
            token_data = json.load(f)
        
        # Verificar expiração
        expires = datetime.fromisoformat(token_data["expires"])
        if datetime.now() > expires:
            return None
        
        return token_data
    
    def cleanup_expired_tokens(self):
        """Remove tokens expirados"""
        for token_file in self.tokens_dir.glob("*.json"):
            with open(token_file, 'r') as f:
                token_data = json.load(f)
            expires = datetime.fromisoformat(token_data["expires"])
            if datetime.now() > expires:
                token_file.unlink()


if __name__ == "__main__":
    # Teste básico
    manager = QRTokenManager("C:/Users/User/Downloads/word-para-medicos/data")
    token = manager.generate_token("prontuario_001", "João Silva")
    print(f"Token gerado: {token}")
    
    qr_path = "C:/Users/User/Downloads/word-para-medicos/data/test_qr.png"
    manager.generate_qr_code(token, qr_path)
    print(f"QR Code salvo em: {qr_path}")
    
    # Validar token
    validated = manager.validate_token(token)
    print(f"Token válido: {validated is not None}")