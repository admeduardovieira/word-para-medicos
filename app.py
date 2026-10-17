#!/usr/bin/env python3
"""
Aplicação Word para Médicos - Interface principal
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Adicionar diretórios ao path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, simpledialog
    from tkinter.scrolledtext import ScrolledText
except ImportError:
    print("tkinter não disponível. Instale python3-tk ou use: python -m pip install tk")
    sys.exit(1)

from core.prontuario import ProntuarioMedico
from core.qr_handler import QRTokenManager


class WordParaMedicosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word para Médicos v1.0")
        self.root.geometry("1000x700")
        
        # Diretórios
        self.app_dir = Path(__file__).parent
        self.data_dir = self.app_dir / "data"
        self.patients_dir = self.data_dir / "patients"
        self.patients_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar componentes
        self.prontuario = ProntuarioMedico()
        self.qr_manager = QRTokenManager(str(self.data_dir))
        
        # Estado atual
        self.current_file = None
        self.paciente_nome = ""
        self.medico_nome = "Dr. Eduardo Vieira"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Menu principal
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Novo Prontuário", command=self.new_prontuario)
        file_menu.add_command(label="Salvar", command=self.save_prontuario)
        file_menu.add_command(label="Salvar Como...", command=self.save_as_prontuario)
        file_menu.add_separator()
        file_menu.add_command(label="Abrir Prontuário", command=self.open_prontuario)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        share_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Compartilhar", menu=share_menu)
        share_menu.add_command(label="Gerar QR Code", command=self.generate_qr)
        share_menu.add_command(label="Ler QR Code", command=self.scan_qr)
        
        # Layout principal com painel lateral
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Editor principal
        self.editor = ScrolledText(main_frame, wrap=tk.WORD, font=('Arial', 11))
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Painel lateral
        sidebar = ttk.Frame(main_frame, width=250)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        sidebar.pack_propagate(False)
        
        # Botões do painel lateral
        btn_novo = ttk.Button(sidebar, text="📄 Novo Prontuário", command=self.new_prontuario)
        btn_novo.pack(fill=tk.X, pady=5)
        
        btn_salvar = ttk.Button(sidebar, text="💾 Salvar", command=self.save_prontuario)
        btn_salvar.pack(fill=tk.X, pady=5)
        
        btn_abrir = ttk.Button(sidebar, text="📂 Abrir", command=self.open_prontuario)
        btn_abrir.pack(fill=tk.X, pady=5)
        
        btn_qr = ttk.Button(sidebar, text="📱 Compartilhar QR", command=self.generate_qr)
        btn_qr.pack(fill=tk.X, pady=5)
        
        btn_scan = ttk.Button(sidebar, text="🔍 Ler QR", command=self.scan_qr)
        btn_scan.pack(fill=tk.X, pady=5)
        
        # Informações do paciente
        info_frame = ttk.LabelFrame(sidebar, text="Informações")
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text=f"Médico: {self.medico_nome}").pack(anchor=tk.W, padx=5)
        ttk.Label(info_frame, text="Data: " + datetime.now().strftime("%d/%m/%Y")).pack(anchor=tk.W, padx=5)
        
        # Área de paciente
        paciente_frame = ttk.LabelFrame(sidebar, text="Paciente")
        paciente_frame.pack(fill=tk.X, pady=5)
        
        self.paciente_var = tk.StringVar()
        paciente_entry = ttk.Entry(paciente_frame, textvariable=self.paciente_var, width=25)
        paciente_entry.pack(padx=5, pady=5)
        
        # Lista de prontuários recentes
        recent_frame = ttk.LabelFrame(sidebar, text="Recentes")
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.recent_listbox = tk.Listbox(recent_frame, height=8)
        self.recent_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.recent_listbox.bind('<Double-Button-1>', self.open_from_list)
        
        self.load_recent_files()
    
    def new_prontuario(self):
        """Cria um novo prontuário"""
        self.prontuario = ProntuarioMedico()
        self.current_file = None
        self.editor.delete(1.0, tk.END)
        
        # Template básico
        template = f"""PRONTUÁRIO MÉDICO

Paciente: {self.paciente_var.get() or "[Nome do Paciente]"}
Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}
Médico: {self.medico_nome}

---

ANAMNESE

Queixa Principal:
[Descreva a queixa principal do paciente]

Histórico:
[Histórico clínico relevante]

Exame Físico:
[Constatações do exame físico]

---

DIAGNÓSTICO
[Suspeita ou diagnóstico confirmado]

---

PRESCRIÇÃO
[Medicamentos prescritos]

---

EVOLUÇÃO
[Acompanhamento e evolução do caso]
"""
        self.editor.insert(1.0, template)
    
    def save_prontuario(self):
        """Salva o prontuário atual"""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_as_prontuario()
    
    def save_as_prontuario(self):
        """Salva como novo arquivo"""
        filename = simpledialog.askstring("Salvar como", "Nome do arquivo (sem extensão):")
        if not filename:
            return
        
        # Criar nome com data
        if not filename.endswith('.docx'):
            filename += '.docx'
        
        filepath = self.patients_dir / filename
        content = self.editor.get(1.0, tk.END)
        
        # Salvar como DOCX
        self.prontuario = ProntuarioMedico()
        # Adicionar conteúdo do editor ao documento
        p = self.prontuario.doc.add_paragraph()
        p.add_run(content)
        
        self.prontuario.save(str(filepath))
        self.current_file = str(filepath)
        messagebox.showinfo("Salvo", f"Prontuário salvo em:\n{filepath}")
        self.load_recent_files()
    
    def open_prontuario(self):
        """Abre um prontuário existente"""
        filepath = filedialog.askopenfilename(
            initialdir=str(self.patients_dir),
            title="Selecione o arquivo",
            filetypes=[("Word Files", "*.docx"), ("All Files", "*.*")]
        )
        
        if filepath:
            self.current_file = filepath
            self.editor.delete(1.0, tk.END)
            
            from docx import Document
            doc = Document(filepath)
            text = "\n".join([p.text for p in doc.paragraphs if p.text])
            self.editor.insert(1.0, text)
            messagebox.showinfo("Aberto", f"Prontuário aberto: {filepath}")
    
    def generate_qr(self):
        """Gera QR Code e abre visualização para compartilhamento imediato"""
        if not self.current_file:
            messagebox.showwarning("Aviso", "Salve o prontuario primeiro!")
            return
        
        # Criar token
        prontuario_id = os.path.basename(self.current_file)
        token = self.qr_manager.generate_token(prontuario_id, self.paciente_var.get())
        
        # Gerar QR Code
        qr_path = self.patients_dir / f"qr_{token}.png"
        self.qr_manager.generate_qr_code(token, str(qr_path))
        
        # Mostrar janela de visualização IMEDIATAMENTE
        self.show_qr_window(token, str(qr_path), prontuario_id)
    
    def show_qr_window(self, token, qr_path, prontuario_id):
        """Mostra janela com QR Code para compartilhamento imediato"""
        qr_window = tk.Toplevel(self.root)
        qr_window.title("QR Code - Compartilhamento Seguro")
        qr_window.geometry("350x400")
        qr_window.transient(self.root)
        qr_window.grab_set()  # Janela modal
        
        # Centralizar na tela
        qr_window.update_idletasks()
        x = (qr_window.winfo_screenwidth() // 2) - (350 // 2)
        y = (qr_window.winfo_screenheight() // 2) - (400 // 2)
        qr_window.geometry(f"350x400+{x}+{y}")
        
        # Título
        tk.Label(qr_window, text="Compartilhar Prontuario via QR Code", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Informações
        tk.Label(qr_window, text=f"Prontuario: {prontuario_id}", 
                font=("Arial", 9)).pack(pady=2)
        tk.Label(qr_window, text=f"Paciente: {self.paciente_var.get()}", 
                font=("Arial", 9)).pack(pady=2)
        
        # Mostrar imagem do QR Code
        try:
            from PIL import Image, ImageTk
            img = Image.open(qr_path)
            img = img.resize((250, 250))
            img_tk = ImageTk.PhotoImage(img)
            
            qr_label = tk.Label(qr_window, image=img_tk)
            qr_label.image = img_tk
            qr_label.pack(pady=10)
        except ImportError:
            tk.Label(qr_window, text="QR Code salvo em:\n" + qr_path, 
                    font=("Arial", 9)).pack(pady=10)
        
        # Token
        tk.Label(qr_window, text=f"Token: {token}", 
                font=("Arial", 8)).pack(pady=2)
        
        # Instrucoes
        tk.Label(qr_window, text="1. Tire um print desta tela\n"
                                "2. Compartilhe com o paciente\n"
                                "3. O prontuario expira em 24h", 
                font=("Arial", 8), fg="gray").pack(pady=10)
        
        # Botao de fechar
        ttk.Button(qr_window, text="Fechar", command=qr_window.destroy).pack(pady=5)
    
    def scan_qr(self):
        """Lê um QR Code"""
        qr_path = filedialog.askopenfilename(
            initialdir=str(self.patients_dir),
            title="Selecione o QR Code",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        
        if not qr_path:
            return
        
        try:
            from pyzbar.pyzbar import decode
            from PIL import Image
            
            img = Image.open(qr_path)
            decoded = decode(img)
            
            if decoded:
                data = decoded[0].data.decode('utf-8')
                if data.startswith("wpm:"):
                    token = data[3:]  # Remove prefixo "wpm:"
                    token_data = self.qr_manager.validate_token(token)
                    
                    if token_data:
                        prontuario_id = token_data["prontuario_id"]
                        prontuario_path = self.patients_dir / prontuario_id
                        
                        if prontuario_path.exists():
                            self.open_file(str(prontuario_path))
                            messagebox.showinfo("Sucesso", "Prontuário acesso via QR Code!")
                        else:
                            messagebox.showerror("Erro", f"Prontuário não encontrado: {prontuario_id}")
                    else:
                        messagebox.showerror("Erro", "Token inválido ou expirado")
                else:
                    messagebox.showinfo("QR Code", f"Dados: {data}")
            else:
                messagebox.showerror("Erro", "Nenhum código QR encontrado na imagem")
                
        except ImportError:
            messagebox.showerror("Erro", "Bibliotecas de leitura de QR Code não instaladas.\nInstale: pip install pyzbar pillow")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler QR Code: {str(e)}")
    
    def open_file(self, filepath):
        """Abre arquivo específico"""
        self.current_file = filepath
        self.editor.delete(1.0, tk.END)
        
        from docx import Document
        doc = Document(filepath)
        text = "\n".join([p.text for p in doc.paragraphs if p.text])
        self.editor.insert(1.0, text)
    
    def open_from_list(self, event):
        """Abre prontuário da lista de recentes"""
        selected = self.recent_listbox.get(tk.ACTIVE)
        if selected:
            filepath = self.patients_dir / selected
            if filepath.exists():
                self.open_file(str(filepath))
    
    def _save_to_file(self, filepath):
        """Salva conteúdo no arquivo especificado"""
        content = self.editor.get(1.0, tk.END)
        self.prontuario = ProntuarioMedico()
        p = self.prontuario.doc.add_paragraph()
        p.add_run(content)
        self.prontuario.save(filepath)
        messagebox.showinfo("Salvo", "Prontuário salvo com sucesso!")
    
    def load_recent_files(self):
        """Carrega lista de prontuários recentes"""
        self.recent_listbox.delete(0, tk.END)
        
        files = sorted(self.patients_dir.glob("*.docx"), key=os.path.getmtime, reverse=True)
        for f in files[:20]:  # Últimos 20 arquivos
            self.recent_listbox.insert(tk.END, f.name)


def main():
    root = tk.Tk()
    app = WordParaMedicosApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()