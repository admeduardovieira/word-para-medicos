#!/usr/bin/env python3
"""
Word para Médicos - Aplicação leve para geração de prontuários médicos em formato DOCX
Compartilhamento seguro via QR Code
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

class ProntuarioMedico:
    """Gerenciador de prontuários médicos em formato DOCX"""
    
    def __init__(self, template_path=None):
        if template_path and os.path.exists(template_path):
            self.doc = Document(template_path)
        else:
            self.doc = Document()
    
    def add_header(self, paciente_nome, data, medico):
        """Adiciona cabeçalho ao prontuário"""
        header = self.doc.sections[0].header
        header.paragraphs[0].text = f"PRONTUÁRIO MÉDICO - {paciente_nome.upper()}"
        
        # Tabela de informações
        table = self.doc.add_table(rows=1, cols=3)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.style = 'Table Grid'
        
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = f"Paciente: {paciente_nome}"
        hdr_cells[1].text = f"Data: {data}"
        hdr_cells[2].text = f"Médico: {medico}"
    
    def add_secao(self, titulo, conteudo=""):
        """Adiciona uma seção ao prontuário"""
        p = self.doc.add_paragraph()
        p.add_run(titulo).bold = True
        p.add_run(f"\n{conteudo}")
    
    def add_anamnese(self, queixa_principal, historico, examem_fisico):
        """Adiciona seção de anamnese"""
        self.add_secao("QUEIXA PRINCIPAL", queixa_principal)
        self.add_secao("HISTÓRICO", historico)
        self.add_secao("EXAME FÍSICO", examem_fisico)
    
    def add_diagnostico(self, diagnosticos):
        """Adiciona seção de diagnóstico"""
        self.add_secao("DIAGNÓSTICO", diagnosticos)
    
    def add_prescricao(self, medicamentos):
        """Adiciona seção de prescrição"""
        self.add_secao("PRESCRIÇÃO", medicamentos)
    
    def add_evolucao(self, evolucao):
        """Adiciona seção de evolução"""
        self.add_secao("EVOLUÇÃO", evolucao)
    
    def save(self, filepath):
        """Salva o prontuário"""
        self.doc.save(filepath)
    
    def load(self, filepath):
        """Carrega prontuário existente"""
        self.doc = Document(filepath)


if __name__ == "__main__":
    # Teste básico
    prontuario = ProntuarioMedico()
    prontuario.add_header("João Silva", "15/01/2025", "Dr. Eduardo Vieira")
    prontuario.add_anamnese(
        "Dor torácica há 3horas",
        "Paciente masculino, 45 anos, sem historico relevante",
        "Paciente em sofrimento, TA 140x90, FC 100bpm"
    )
    prontuario.add_diagnostico("Síndrome torácica")
    prontuario.add_prescricao("Aspirina 100mg 1x ao dia")
    prontuario.add_evolucao("Paciente evoluindo bem com tratamento")
    
    output_path = Path("C:/Users/User/Downloads/word-para-medicos/data/patients/test_prontuario.docx")
    prontuario.save(str(output_path))
    print(f"Prontuário salvo em: {output_path}")