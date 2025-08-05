#!/usr/bin/env python3
"""
Conversor Excel → XML - Sistema Banco do Brasil
Aplicação desktop para converter planilhas Excel em arquivos XML
Versão para Ubuntu/Linux
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os
from pathlib import Path
import traceback
import threading
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("Iniciando Conversor Excel → XML (Desktop)...")

try:
    from gui.main_window import MainWindow
    from services.data_manager import DataManager
    from services.excel_processor import ExcelProcessor
    from services.xml_generator import XMLGenerator
    from models.responsible import Responsible
    from utils.validators import validate_cpf
    from utils.constants import PROFILES, PROFILE_TYPES
    print("✓ Imports bem-sucedidos")
except Exception as e:
    print(f"✗ Erro no import: {e}")
    traceback.print_exc()
    exit(1)

class DesktopConversorApp:
    def __init__(self):
        print("Inicializando aplicação desktop...")
        try:
            # Configurar estilo GTK para Ubuntu
            self.setup_linux_style()
            
            self.root = tk.Tk()
            self.root.title("Conversor Excel → XML - Sistema BB v2.0")
            self.root.geometry("1200x800")
            self.root.minsize(1000, 600)
            print("✓ Janela Tkinter criada")
            
            # Inicializar serviços
            self.data_manager = DataManager()
            self.excel_processor = ExcelProcessor()
            self.xml_generator = XMLGenerator()
            print("✓ Serviços inicializados")
            
            # Configurar interface
            self.setup_ui()
            print("✓ Interface configurada")
            
            # Configurar propriedades da janela
            self.root.configure(bg='#f0f0f0')
            
            # Centralizar janela
            self.center_window()
            print("✓ Janela centralizada")
            
            print("Aplicação desktop inicializada com sucesso!")
            
        except Exception as e:
            print(f"✗ Falha na inicialização: {e}")
            traceback.print_exc()
            raise
    
    def setup_linux_style(self):
        """Configurar estilo específico para Linux/Ubuntu"""
        try:
            # Tentar usar tema nativo do sistema
            style = ttk.Style()
            available_themes = style.theme_names()
            print(f"Temas disponíveis: {available_themes}")
            
            # Preferir temas que funcionam bem no Ubuntu
            preferred_themes = ['clam', 'alt', 'default', 'classic']
            selected_theme = 'default'
            
            for theme in preferred_themes:
                if theme in available_themes:
                    selected_theme = theme
                    break
            
            style.theme_use(selected_theme)
            print(f"✓ Usando tema: {selected_theme}")
            
        except Exception as e:
            print(f"Aviso: Não foi possível configurar tema: {e}")
    
    def setup_ui(self):
        """Configurar interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos da grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=7)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(1, weight=1)
        
        # Cabeçalho
        self.setup_header(main_frame)
        
        # Área de conteúdo principal (70%)
        self.setup_main_content(main_frame)
        
        # Barra lateral (30%)
        self.setup_sidebar(main_frame)
        
        # Barra de status
        self.setup_status_bar(main_frame)
    
    def setup_header(self, parent):
        """Configurar cabeçalho"""
        header_frame = ttk.Frame(parent, padding="0 0 20 0")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Título
        title_label = ttk.Label(header_frame, text="Conversor Excel → XML - Sistema BB v2.0", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtítulo
        subtitle_label = ttk.Label(header_frame, text="Sistema de Comandos de Pagamento Banco do Brasil", 
                                  font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
    
    def setup_main_content(self, parent):
        """Configurar área de conteúdo principal"""
        # Frame de conteúdo principal
        content_frame = ttk.LabelFrame(parent, text="Conversão de Arquivo", padding="20")
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        
        # Área de upload de arquivo
        self.setup_upload_area(content_frame)
        
        # Área de formulário
        self.setup_form_area(content_frame)
        
        # Área de progresso
        self.setup_progress_area(content_frame)
        
        # Botões de ação
        self.setup_action_buttons(content_frame)
    
    def setup_upload_area(self, parent):
        """Configurar área de upload"""
        upload_frame = ttk.LabelFrame(parent, text="📁 Seleção de Arquivo", padding="20")
        upload_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        upload_frame.columnconfigure(0, weight=1)
        
        # Área de seleção de arquivo
        self.file_area = ttk.Frame(upload_frame, relief="solid", borderwidth=2)
        self.file_area.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.file_area.columnconfigure(0, weight=1)
        
        # Label de instruções
        instruction_label = ttk.Label(self.file_area, 
                                     text="📄 Clique aqui para selecionar um arquivo Excel\n\nFormatos suportados: .xlsx, .xls", 
                                     anchor="center",
                                     font=("Arial", 12))
        instruction_label.grid(row=0, column=0, pady=40, padx=20)
        
        # Fazer a área clicável
        self.file_area.bind("<Button-1>", self.select_file)
        instruction_label.bind("<Button-1>", self.select_file)
        
        # Botões de arquivo
        button_frame = ttk.Frame(upload_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="📂 Selecionar Arquivo", 
                  command=self.select_file).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="📥 Baixar Modelo Excel", 
                  command=self.download_template).grid(row=0, column=1)
        
        # Informações do arquivo
        self.file_info_label = ttk.Label(upload_frame, text="Nenhum arquivo selecionado", 
                                        foreground="gray")
        self.file_info_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    
    def setup_form_area(self, parent):
        """Configurar área de formulário"""
        form_frame = ttk.LabelFrame(parent, text="⚙️ Configurações", padding="20")
        form_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        form_frame.columnconfigure(1, weight=1)
        
        # Seleção de responsável
        ttk.Label(form_frame, text="Responsável:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.responsible_var = tk.StringVar()
        self.responsible_combo = ttk.Combobox(form_frame, textvariable=self.responsible_var, 
                                             state="readonly", width=40)
        self.responsible_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.responsible_combo.bind('<<ComboboxSelected>>', self.on_responsible_selected)
        
        # Nome do arquivo de saída
        ttk.Label(form_frame, text="Nome do arquivo XML:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.output_filename_var = tk.StringVar(value="comandos_pagamento.xml")
        ttk.Entry(form_frame, textvariable=self.output_filename_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Folha (mês/ano)
        ttk.Label(form_frame, text="Folha (MMAAAA):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.folha_var = tk.StringVar()
        folha_entry = ttk.Entry(form_frame, textvariable=self.folha_var, width=10)
        folha_entry.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        
        # Adicionar validação
        vcmd = (self.root.register(self.validate_folha), '%P')
        folha_entry.config(validate='key', validatecommand=vcmd)
    
    def setup_progress_area(self, parent):
        """Configurar área de progresso"""
        progress_frame = ttk.LabelFrame(parent, text="📊 Status", padding="20")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Mensagens de status
        self.status_text = tk.Text(progress_frame, height=6, wrap=tk.WORD)
        self.status_text.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar para texto de status
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.status_text.config(yscrollcommand=scrollbar.set)
    
    def setup_action_buttons(self, parent):
        """Configurar botões de ação"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Botão converter
        self.convert_button = ttk.Button(button_frame, text="🔄 Converter para XML", 
                                        command=self.convert_file, state=tk.DISABLED)
        self.convert_button.grid(row=0, column=0, padx=(0, 10))
        
        # Botão limpar
        ttk.Button(button_frame, text="🗑️ Limpar", 
                  command=self.clear_form).grid(row=0, column=1, padx=(0, 10))
        
        # Botão ajuda
        ttk.Button(button_frame, text="❓ Ajuda", 
                  command=self.show_help).grid(row=0, column=2)
    
    def setup_sidebar(self, parent):
        """Configurar barra lateral"""
        sidebar_frame = ttk.LabelFrame(parent, text="👥 Responsáveis", padding="20")
        sidebar_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        sidebar_frame.columnconfigure(0, weight=1)
        
        # Botão para adicionar responsável
        ttk.Button(sidebar_frame, text="➕ Novo Responsável", 
                  command=self.add_responsible).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Lista de responsáveis
        self.responsibles_listbox = tk.Listbox(sidebar_frame, height=10)
        self.responsibles_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Scrollbar para lista
        list_scrollbar = ttk.Scrollbar(sidebar_frame, orient=tk.VERTICAL, command=self.responsibles_listbox.yview)
        list_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.responsibles_listbox.config(yscrollcommand=list_scrollbar.set)
        
        # Botões de gerenciamento
        mgmt_frame = ttk.Frame(sidebar_frame)
        mgmt_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(mgmt_frame, text="✏️ Editar", 
                  command=self.edit_responsible).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(mgmt_frame, text="🗑️ Remover", 
                  command=self.remove_responsible).grid(row=0, column=1)
    
    def setup_status_bar(self, parent):
        """Configurar barra de status"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_bar_label = ttk.Label(status_frame, text="Pronto", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
    
    def center_window(self):
        """Centralizar janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_responsibles(self):
        """Carregar responsáveis"""
        try:
            responsibles = self.data_manager.get_responsibles()
            
            # Atualizar combobox
            combo_values = [f"{r.nome} - {r.cpf}" for r in responsibles]
            self.responsible_combo['values'] = combo_values
            
            # Atualizar listbox
            self.responsibles_listbox.delete(0, tk.END)
            for responsible in responsibles:
                display_text = f"{responsible.nome}\nCPF: {responsible.cpf}\nPerfil: {responsible.perfil}"
                self.responsibles_listbox.insert(tk.END, display_text)
                
            self.update_status(f"Carregados {len(responsibles)} responsáveis")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar responsáveis: {str(e)}")
    
    def select_file(self, event=None):
        """Selecionar arquivo Excel"""
        filetypes = [
            ("Excel files", "*.xlsx *.xls"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo Excel",
            filetypes=filetypes
        )
        
        if filename:
            self.process_selected_file(filename)
    
    def process_selected_file(self, filename):
        """Processar arquivo selecionado"""
        try:
            self.selected_file = filename
            
            # Atualizar interface
            file_info = f"Arquivo: {Path(filename).name}"
            self.file_info_label.config(text=file_info, foreground="black")
            
            # Processar arquivo em thread separada para não travar a interface
            self.update_status("Processando arquivo...")
            self.progress_var.set(20)
            
            threading.Thread(target=self.process_file_thread, args=(filename,), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar arquivo: {str(e)}")
    
    def process_file_thread(self, filename):
        """Processar arquivo em thread separada"""
        try:
            # Processar arquivo Excel
            self.processed_data = self.excel_processor.process_file(filename)
            
            # Atualizar interface na thread principal
            self.root.after(0, self.on_file_processed, len(self.processed_data))
            
        except Exception as e:
            self.root.after(0, self.on_file_error, str(e))
    
    def on_file_processed(self, record_count):
        """Callback quando arquivo foi processado"""
        self.progress_var.set(50)
        self.update_status(f"Arquivo processado com sucesso! {record_count} registros encontrados.")
        self.update_convert_button()
    
    def on_file_error(self, error_msg):
        """Callback quando houve erro no processamento"""
        self.progress_var.set(0)
        self.update_status(f"Erro: {error_msg}")
        messagebox.showerror("Erro", f"Erro ao processar arquivo: {error_msg}")
    
    def convert_file(self):
        """Converter arquivo para XML"""
        try:
            if not hasattr(self, 'selected_file') or not self.selected_file:
                messagebox.showerror("Erro", "Selecione um arquivo primeiro")
                return
                
            if not hasattr(self, 'processed_data') or not self.processed_data:
                messagebox.showerror("Erro", "Nenhum dado processado encontrado")
                return
            
            # Validar responsável
            responsible_text = self.responsible_var.get()
            if not responsible_text:
                messagebox.showerror("Erro", "Selecione um responsável")
                return
            
            # Obter responsável selecionado
            responsibles = self.data_manager.get_responsibles()
            selected_responsible = None
            for responsible in responsibles:
                if f"{responsible.nome} - {responsible.cpf}" == responsible_text:
                    selected_responsible = responsible
                    break
            
            if not selected_responsible:
                messagebox.showerror("Erro", "Responsável não encontrado")
                return
            
            # Validar folha
            folha = self.folha_var.get().strip()
            if not folha or len(folha) != 6:
                messagebox.showerror("Erro", "Informe a folha no formato MMAAAA (ex: 012024)")
                return
            
            # Iniciar conversão
            self.update_status("Convertendo para XML...")
            self.progress_var.set(70)
            
            # Gerar XML
            xml_content = self.xml_generator.generate_xml(self.processed_data, selected_responsible, folha)
            
            # Salvar arquivo
            output_filename = self.output_filename_var.get().strip()
            if not output_filename:
                output_filename = "comandos_pagamento.xml"
            elif not output_filename.endswith('.xml'):
                output_filename += '.xml'
            
            save_path = filedialog.asksaveasfilename(
                title="Salvar arquivo XML",
                defaultextension=".xml",
                filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
                initialvalue=output_filename
            )
            
            if save_path:
                with open(save_path, 'w', encoding='iso-8859-1') as f:
                    f.write(xml_content)
                
                self.progress_var.set(100)
                self.update_status(f"Conversão concluída! Arquivo salvo em: {save_path}")
                messagebox.showinfo("Sucesso", f"XML gerado com sucesso!\n\nArquivo salvo em:\n{save_path}")
            
        except Exception as e:
            self.progress_var.set(0)
            error_msg = f"Erro na conversão: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("Erro", error_msg)
    
    def clear_form(self):
        """Limpar formulário"""
        self.selected_file = None
        self.processed_data = None
        self.file_info_label.config(text="Nenhum arquivo selecionado", foreground="gray")
        self.responsible_var.set("")
        self.output_filename_var.set("comandos_pagamento.xml")
        self.folha_var.set("")
        self.progress_var.set(0)
        self.status_text.delete(1.0, tk.END)
        self.update_convert_button()
        self.update_status("Pronto")
    
    def validate_folha(self, value):
        """Validar entrada da folha"""
        if len(value) > 6:
            return False
        return value.isdigit()
    
    def on_responsible_selected(self, event=None):
        """Callback quando responsável é selecionado"""
        self.update_convert_button()
    
    def update_convert_button(self):
        """Atualizar estado do botão converter"""
        has_file = hasattr(self, 'selected_file') and self.selected_file
        has_responsible = bool(self.responsible_var.get())
        has_folha = len(self.folha_var.get()) == 6
        
        if has_file and has_responsible and has_folha:
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.convert_button.config(state=tk.DISABLED)
    
    def add_responsible(self):
        """Adicionar novo responsável"""
        from gui.widgets import ResponsibleDialog
        
        dialog = ResponsibleDialog(self.root, "Novo Responsável")
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                self.data_manager.add_responsible(dialog.result)
                self.load_responsibles()
                messagebox.showinfo("Sucesso", "Responsável adicionado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar responsável: {str(e)}")
    
    def edit_responsible(self):
        """Editar responsável selecionado"""
        selection = self.responsibles_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um responsável para editar")
            return
        
        # Implementar edição (similar ao add_responsible)
        messagebox.showinfo("Info", "Funcionalidade de edição será implementada em breve")
    
    def remove_responsible(self):
        """Remover responsável selecionado"""
        selection = self.responsibles_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um responsável para remover")
            return
        
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este responsável?"):
            try:
                index = selection[0]
                responsibles = self.data_manager.get_responsibles()
                if index < len(responsibles):
                    responsible = responsibles[index]
                    self.data_manager.remove_responsible(responsible.id)
                    self.load_responsibles()
                    messagebox.showinfo("Sucesso", "Responsável removido com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover responsável: {str(e)}")
    
    def download_template(self):
        """Baixar modelo Excel"""
        try:
            save_path = filedialog.asksaveasfilename(
                title="Salvar modelo Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialvalue="modelo_excel.xlsx"
            )
            
            if save_path:
                self.excel_processor.create_template(save_path)
                messagebox.showinfo("Sucesso", f"Modelo Excel criado em:\n{save_path}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar modelo: {str(e)}")
    
    def show_help(self):
        """Mostrar ajuda"""
        help_text = """
Conversor Excel → XML - Sistema Banco do Brasil

COMO USAR:

1. SELECIONAR ARQUIVO
   • Clique em "Selecionar Arquivo" ou na área indicada
   • Escolha um arquivo Excel (.xlsx ou .xls)

2. CONFIGURAR RESPONSÁVEL
   • Selecione um responsável da lista
   • Para adicionar novo: clique em "Novo Responsável"

3. INFORMAR FOLHA
   • Digite no formato MMAAAA
   • Exemplo: 012024 para Janeiro/2024

4. CONVERTER
   • Clique em "Converter para XML"
   • Escolha onde salvar o arquivo

FORMATO DO EXCEL:
• Colunas obrigatórias: matricula, rubrica, valor, tipo, trigrama
• Use o botão "Baixar Modelo Excel" para ter um exemplo

SUPORTE:
• Formato de saída: XML Banco do Brasil
• Validação automática de dados
• Backup automático de configurações
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Ajuda")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Centralizar janela de ajuda
        help_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_help = ttk.Scrollbar(help_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar_help.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar_help.set)
        
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Fechar", 
                  command=help_window.destroy).pack(pady=10)
    
    def update_status(self, message):
        """Atualizar status"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_message = f"[{timestamp}] {message}"
        
        # Atualizar barra de status
        self.status_bar_label.config(text=message)
        
        # Adicionar ao log de status
        self.status_text.insert(tk.END, status_message + "\n")
        self.status_text.see(tk.END)
        
        # Atualizar interface
        self.root.update_idletasks()
    
    def run(self):
        """Executar aplicação"""
        try:
            # Carregar responsáveis
            self.load_responsibles()
            
            # Iniciar loop principal
            print("Iniciando loop principal da aplicação...")
            self.root.mainloop()
            
        except KeyboardInterrupt:
            print("Aplicação interrompida pelo usuário")
        except Exception as e:
            print(f"✗ Erro durante execução: {e}")
            traceback.print_exc()
            try:
                messagebox.showerror("Erro Fatal", f"Erro inesperado: {str(e)}")
            except:
                pass

if __name__ == "__main__":
    try:
        app = DesktopConversorApp()
        app.run()
    except Exception as e:
        print(f"✗ Erro fatal: {e}")
        traceback.print_exc()
        input("Pressione Enter para sair...")