#!/usr/bin/env python3
"""
Testes básicos para Word para Médicos
"""

import os
import sys
import tempfile
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent))

from core.prontuario import ProntuarioMedico
from core.qr_handler import QRTokenManager


def test_prontuario_creation():
    """Testa criação de prontuário básico"""
    prontuario = ProntuarioMedico()
    prontuario.add_header("Teste Paciente", "15/01/2025", "Dr. Teste")
    prontuario.add_anamnese(
        "Dor de cabeça",
        "Paciente com historico de hipertensão",
        "PA 140x90, ausculta normal"
    )
    prontuario.add_diagnostico("Hipertensão arterial sistêmica")
    prontuario.add_prescricao("Losartana 50mg 1x ao dia")
    prontuario.add_evolucao("Paciente evoluindo bem")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_prontuario.docx"
        prontuario.save(str(filepath))
        
        assert filepath.exists(), "Arquivo não foi criado"
        assert filepath.stat().st_size > 0, "Arquivo está vazio"
        
        # Carregar e verificar
        loaded = ProntuarioMedico()
        loaded.load(str(filepath))
        paragraphs = [p.text for p in loaded.doc.paragraphs if p.text]
        assert len(paragraphs) > 0, "Documento vazio após carregar"
        assert "Teste Paciente" in paragraphs[0], "Nome do paciente não encontrado"
    
    print("✓ test_prontuario_creation PASSOU")


def test_qr_generation():
    """Testa geração de QR Code"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = QRTokenManager(tmpdir)
        token = manager.generate_token("test_prontuario.docx", "Paciente Teste")
        
        assert len(token) == 32, f"Token deve ter 32 chars, tem {len(token)}"
        
        qr_path = Path(tmpdir) / "test_qr.png"
        result = manager.generate_qr_code(token, str(qr_path))
        
        assert qr_path.exists(), "QR Code não foi criado"
        assert qr_path.stat().st_size > 0, "QR Code está vazio"
        
        # Validar token
        token_data = manager.validate_token(token)
        assert token_data is not None, "Token inválido"
        assert token_data["prontuario_id"] == "test_prontuario.docx", "ID do prontuário não confere"
    
    print("✓ test_qr_generation PASSOU")


def test_token_expiration():
    """Testa expiração de tokens"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = QRTokenManager(tmpdir)
        token = manager.generate_token("test.docx", "Paciente", expires_hours=0)
        
        # Token com 0 horas de duração deve expirar imediatamente
        import time
        time.sleep(1)
        result = manager.validate_token(token)
        assert result is None, "Token deveria estar expirado"
    
    print("✓ test_token_expiration PASSOU")


def test_docx_format():
    """Verifica se o DOCX tem formatação adequada"""
    prontuario = ProntuarioMedico()
    prontuario.add_header("Formato Teste", "15/01/2025", "Dr. Teste")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "format_test.docx"
        prontuario.save(str(filepath))
        
        # Verificar se é um arquivo DOCX válido
        import zipfile
        assert zipfile.is_zipfile(str(filepath)), "Arquivo não é um DOCX válido"
        
        # Verificar conteúdo
        with zipfile.ZipFile(str(filepath), 'r') as zf:
            names = zf.namelist()
            assert 'word/document.xml' in names, "Documento XML não encontrado"
    
    print("✓ test_docx_format PASSOU")


if __name__ == "__main__":
    test_prontuario_creation()
    test_qr_generation()
    test_token_expiration()
    test_docx_format()
    print("\n=== Todos os testes PASSARAM ===")