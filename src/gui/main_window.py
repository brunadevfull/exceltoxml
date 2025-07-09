"""
Main window GUI for the Excel to XML converter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import os

from .widgets import *
from models.responsible import Responsible
from services.excel_processor import ExcelProcessor
from services.xml_generator import XMLGenerator
from utils.validators import validate_cpf
from utils.constants import PROFILES, PROFILE_TYPES

class MainWindow:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        self.selected_file = None
        self.current_responsible = None
        self.processed_data = None
        
        # Initialize processors
        self.excel_processor = ExcelProcessor()
        self.xml_generator = XMLGenerator()
        
        self.setup_ui()
        self.load_responsibles()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=7)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        self.setup_header(main_frame)
        
        # Main content area (70%)
        self.setup_main_content(main_frame)
        
        # Sidebar (30%)
        self.setup_sidebar(main_frame)
        
        # Status bar
        self.setup_status_bar(main_frame)
        
    def setup_header(self, parent):
        """Setup header with title and logo"""
        header_frame = ttk.Frame(parent, padding="0 0 20 0")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Title
        title_label = ttk.Label(header_frame, text="Conversor Excel → XML - Sistema BB v2.0", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Sistema de Comandos de Pagamento Banco do Brasil", 
                                  font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
    def setup_main_content(self, parent):
        """Setup main content area"""
        # Main content frame
        content_frame = ttk.LabelFrame(parent, text="Conversão de Arquivo", padding="20")
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        
        # File upload area
        self.setup_file_upload(content_frame)
        
        # Form area
        self.setup_form_area(content_frame)
        
        # Progress area
        self.setup_progress_area(content_frame)
        
        # Action buttons
        self.setup_action_buttons(content_frame)
        
    def setup_file_upload(self, parent):
        """Setup file upload area with drag and drop"""
        upload_frame = ttk.LabelFrame(parent, text="📁 Arquivo Excel", padding="20")
        upload_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        upload_frame.columnconfigure(0, weight=1)
        
        # File drop area
        self.file_drop_area = FileDropArea(upload_frame, self.on_file_selected)
        self.file_drop_area.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # File buttons
        button_frame = ttk.Frame(upload_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="📂 Selecionar Arquivo", 
                  command=self.select_file).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="📥 Baixar Modelo Excel", 
                  command=self.download_template).grid(row=0, column=1)
        
        # File info
        self.file_info_label = ttk.Label(upload_frame, text="Nenhum arquivo selecionado", 
                                        foreground="gray")
        self.file_info_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        
    def setup_form_area(self, parent):
        """Setup form input area"""
        form_frame = ttk.LabelFrame(parent, text="⚙️ Configurações", padding="20")
        form_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        form_frame.columnconfigure(1, weight=1)
        
        # Responsible selection
        ttk.Label(form_frame, text="Responsável:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.responsible_var = tk.StringVar()
        self.responsible_combo = ttk.Combobox(form_frame, textvariable=self.responsible_var, 
                                             state="readonly", width=40)
        self.responsible_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.responsible_combo.bind('<<ComboboxSelected>>', self.on_responsible_selected)
        
        # Output filename
        ttk.Label(form_frame, text="Nome do arquivo XML:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.output_filename_var = tk.StringVar(value="comandos_pagamento.xml")
        ttk.Entry(form_frame, textvariable=self.output_filename_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Folha (month/year)
        ttk.Label(form_frame, text="Folha (MMAAAA):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.folha_var = tk.StringVar()
        folha_entry = ttk.Entry(form_frame, textvariable=self.folha_var, width=10)
        folha_entry.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        
        # Add validation
        vcmd = (self.root.register(self.validate_folha), '%P')
        folha_entry.config(validate='key', validatecommand=vcmd)
        
    def setup_progress_area(self, parent):
        """Setup progress and status area"""
        progress_frame = ttk.LabelFrame(parent, text="📊 Status", padding="20")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status messages
        self.status_text = tk.Text(progress_frame, height=6, wrap=tk.WORD)
        self.status_text.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.status_text.config(yscrollcommand=scrollbar.set)
        
    def setup_action_buttons(self, parent):
        """Setup action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Convert button
        self.convert_button = ttk.Button(button_frame, text="🔄 Converter para XML", 
                                        command=self.convert_file, state=tk.DISABLED)
        self.convert_button.grid(row=0, column=0, padx=(0, 10))
        
        # Clear button
        ttk.Button(button_frame, text="🗑️ Limpar", 
                  command=self.clear_form).grid(row=0, column=1, padx=(0, 10))
        
        # Help button
        ttk.Button(button_frame, text="❓ Ajuda", 
                  command=self.show_help).grid(row=0, column=2)
        
    def setup_sidebar(self, parent):
        """Setup sidebar with responsible management"""
        sidebar_frame = ttk.LabelFrame(parent, text="👥 Gerenciar Responsáveis", padding="20")
        sidebar_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        sidebar_frame.columnconfigure(0, weight=1)
        
        # Responsible list
        self.responsible_listbox = tk.Listbox(sidebar_frame, height=15)
        self.responsible_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.responsible_listbox.bind('<<ListboxSelect>>', self.on_responsible_list_select)
        
        # Responsible management buttons
        button_frame = ttk.Frame(sidebar_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="➕ Adicionar", 
                  command=self.add_responsible).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(button_frame, text="✏️ Editar", 
                  command=self.edit_responsible).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(button_frame, text="🗑️ Remover", 
                  command=self.remove_responsible).grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
    def setup_status_bar(self, parent):
        """Setup status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        self.status_label = ttk.Label(status_frame, text="Pronto")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
    def load_responsibles(self):
        """Load responsibles from data manager"""
        responsibles = self.data_manager.get_responsibles()
        
        # Update combo box
        names = [f"{r.nome} - {r.cpf}" for r in responsibles]
        self.responsible_combo['values'] = names
        
        # Update listbox
        self.responsible_listbox.delete(0, tk.END)
        for responsible in responsibles:
            self.responsible_listbox.insert(tk.END, f"{responsible.nome} - {responsible.cpf}")
        
        # Select first if available
        if responsibles:
            self.responsible_combo.current(0)
            self.current_responsible = responsibles[0]
            
    def on_file_selected(self, file_path):
        """Handle file selection"""
        self.selected_file = file_path
        self.file_info_label.config(text=f"Arquivo: {Path(file_path).name}", foreground="green")
        self.update_convert_button_state()
        
        # Process file in background
        self.add_status_message(f"Processando arquivo: {Path(file_path).name}")
        threading.Thread(target=self.process_file, daemon=True).start()
        
    def process_file(self):
        """Process the selected Excel file"""
        try:
            self.progress_var.set(20)
            self.processed_data = self.excel_processor.process_file(self.selected_file)
            self.progress_var.set(50)
            
            # Update status
            self.add_status_message(f"✅ Arquivo processado com sucesso!")
            self.add_status_message(f"📊 Total de registros: {len(self.processed_data)}")
            
            # Validate data
            valid_count = sum(1 for record in self.processed_data if record.get('valid', True))
            invalid_count = len(self.processed_data) - valid_count
            
            if invalid_count > 0:
                self.add_status_message(f"⚠️ Registros inválidos: {invalid_count}")
            
            self.progress_var.set(100)
            
        except Exception as e:
            self.add_status_message(f"❌ Erro ao processar arquivo: {str(e)}")
            self.progress_var.set(0)
            
    def select_file(self):
        """Open file dialog to select Excel file"""
        filetypes = [
            ("Excel files", "*.xlsx *.xls"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo Excel",
            filetypes=filetypes
        )
        
        if filename:
            self.on_file_selected(filename)
            
    def download_template(self):
        """Download Excel template"""
        # Ask where to save
        filename = filedialog.asksaveasfilename(
            title="Salvar modelo Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if filename:
            try:
                self.excel_processor.create_template(filename)
                self.add_status_message(f"✅ Modelo salvo em: {filename}")
                messagebox.showinfo("Sucesso", "Modelo Excel criado com sucesso!")
            except Exception as e:
                self.add_status_message(f"❌ Erro ao criar modelo: {str(e)}")
                messagebox.showerror("Erro", f"Erro ao criar modelo: {str(e)}")
                
    def convert_file(self):
        """Convert Excel file to XML"""
        if not self.validate_form():
            return
            
        # Ask where to save XML
        filename = filedialog.asksaveasfilename(
            title="Salvar arquivo XML",
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml")]
        )
        
        if filename:
            threading.Thread(target=self.perform_conversion, args=(filename,), daemon=True).start()
            
    def perform_conversion(self, output_filename):
        """Perform the actual conversion"""
        try:
            self.progress_var.set(0)
            self.add_status_message("🔄 Iniciando conversão...")
            
            # Generate XML
            xml_content = self.xml_generator.generate_xml(
                self.processed_data,
                self.current_responsible,
                self.folha_var.get()
            )
            
            self.progress_var.set(80)
            
            # Save XML file
            with open(output_filename, 'w', encoding='iso-8859-1') as f:
                f.write(xml_content)
                
            self.progress_var.set(100)
            self.add_status_message(f"✅ Conversão concluída com sucesso!")
            self.add_status_message(f"📄 Arquivo salvo: {output_filename}")
            
            messagebox.showinfo("Sucesso", "Conversão concluída com sucesso!")
            
        except Exception as e:
            self.add_status_message(f"❌ Erro na conversão: {str(e)}")
            messagebox.showerror("Erro", f"Erro na conversão: {str(e)}")
            self.progress_var.set(0)
            
    def validate_form(self):
        """Validate form inputs"""
        if not self.selected_file:
            messagebox.showerror("Erro", "Selecione um arquivo Excel")
            return False
            
        if not self.current_responsible:
            messagebox.showerror("Erro", "Selecione um responsável")
            return False
            
        if not self.folha_var.get():
            messagebox.showerror("Erro", "Informe a folha (MMAAAA)")
            return False
            
        if not self.output_filename_var.get():
            messagebox.showerror("Erro", "Informe o nome do arquivo XML")
            return False
            
        return True
        
    def validate_folha(self, value):
        """Validate folha format (MMAAAA)"""
        if len(value) > 6:
            return False
        return value.isdigit()
        
    def add_status_message(self, message):
        """Add message to status text area"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        
    def update_convert_button_state(self):
        """Update convert button state based on form validation"""
        if (self.selected_file and self.current_responsible and 
            self.folha_var.get() and self.output_filename_var.get()):
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.convert_button.config(state=tk.DISABLED)
            
    def clear_form(self):
        """Clear form inputs"""
        self.selected_file = None
        self.processed_data = None
        self.file_info_label.config(text="Nenhum arquivo selecionado", foreground="gray")
        self.progress_var.set(0)
        self.status_text.delete(1.0, tk.END)
        self.update_convert_button_state()
        
    def show_help(self):
        """Show help dialog"""
        help_text = """
AJUDA - Conversor Excel → XML

1. SELECIONAR ARQUIVO:
   - Clique em "Selecionar Arquivo" ou arraste um arquivo Excel
   - Formatos suportados: .xlsx, .xls

2. CONFIGURAR RESPONSÁVEL:
   - Selecione um responsável cadastrado
   - Para adicionar novo responsável, use a área "Gerenciar Responsáveis"

3. DEFINIR PARÂMETROS:
   - Nome do arquivo XML de saída
   - Folha no formato MMAAAA (ex: 062025 para junho/2025)

4. CONVERTER:
   - Clique em "Converter para XML"
   - Escolha onde salvar o arquivo XML

FORMATO DO EXCEL:
- Colunas obrigatórias: matricula, rubrica, valor, tipo, trigrama
- Tipos: NO (normal) ou DE (desconto)
- Valores: usar ponto ou vírgula como separador decimal

Para mais informações, consulte o manual do usuário.
        """
        
        messagebox.showinfo("Ajuda", help_text)
        
    def on_responsible_selected(self, event):
        """Handle responsible selection from combo"""
        selection = self.responsible_combo.get()
        if selection:
            cpf = selection.split(" - ")[1]
            responsibles = self.data_manager.get_responsibles()
            self.current_responsible = next((r for r in responsibles if r.cpf == cpf), None)
            self.update_convert_button_state()
            
    def on_responsible_list_select(self, event):
        """Handle responsible selection from listbox"""
        selection = self.responsible_listbox.curselection()
        if selection:
            index = selection[0]
            responsibles = self.data_manager.get_responsibles()
            if index < len(responsibles):
                self.current_responsible = responsibles[index]
                self.responsible_combo.set(f"{self.current_responsible.nome} - {self.current_responsible.cpf}")
                self.update_convert_button_state()
                
    def add_responsible(self):
        """Add new responsible"""
        dialog = ResponsibleDialog(self.root, "Adicionar Responsável")
        if dialog.result:
            try:
                self.data_manager.add_responsible(dialog.result)
                self.load_responsibles()
                self.add_status_message(f"✅ Responsável adicionado: {dialog.result.nome}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar responsável: {str(e)}")
                
    def edit_responsible(self):
        """Edit selected responsible"""
        if not self.current_responsible:
            messagebox.showwarning("Aviso", "Selecione um responsável para editar")
            return
            
        dialog = ResponsibleDialog(self.root, "Editar Responsável", self.current_responsible)
        if dialog.result:
            try:
                self.data_manager.update_responsible(self.current_responsible.id, dialog.result)
                self.load_responsibles()
                self.add_status_message(f"✅ Responsável atualizado: {dialog.result.nome}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar responsável: {str(e)}")
                
    def remove_responsible(self):
        """Remove selected responsible"""
        if not self.current_responsible:
            messagebox.showwarning("Aviso", "Selecione um responsável para remover")
            return
            
        if messagebox.askyesno("Confirmar", f"Remover responsável {self.current_responsible.nome}?"):
            try:
                self.data_manager.remove_responsible(self.current_responsible.id)
                self.load_responsibles()
                self.current_responsible = None
                self.responsible_combo.set("")
                self.add_status_message(f"✅ Responsável removido")
                self.update_convert_button_state()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover responsável: {str(e)}")
