"""
Custom widgets for the Excel to XML converter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from pathlib import Path

from models.responsible import Responsible
from utils.validators import validate_cpf
from utils.constants import PROFILES, PROFILE_TYPES

class FileDropArea(ttk.Frame):
    """Custom file selection area widget"""
    
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the file selection area UI"""
        self.configure(relief="solid", borderwidth=2)
        
        # Create a frame for the content
        content_frame = ttk.Frame(self)
        content_frame.pack(expand=True, fill="both", padx=20, pady=40)
        
        # File icon and text
        icon_label = ttk.Label(content_frame, text="📁", font=("Arial", 24))
        icon_label.pack(pady=(0, 10))
        
        # Instructions
        instruction_label = ttk.Label(content_frame, 
                                     text="Clique aqui para selecionar um arquivo Excel", 
                                     font=("Arial", 12, "bold"))
        instruction_label.pack(pady=(0, 5))
        
        # Format info
        format_label = ttk.Label(content_frame, 
                                text="Formatos suportados: .xlsx, .xls", 
                                font=("Arial", 10),
                                foreground="gray")
        format_label.pack()
        
        # Make the entire area clickable
        self.bind("<Button-1>", self.on_click)
        content_frame.bind("<Button-1>", self.on_click)
        icon_label.bind("<Button-1>", self.on_click)
        instruction_label.bind("<Button-1>", self.on_click)
        format_label.bind("<Button-1>", self.on_click)
        
        # Configure cursor
        self.configure(cursor="hand2")
        content_frame.configure(cursor="hand2")
        
    def on_click(self, event):
        """Handle click to select file"""
        filetypes = [
            ("Excel files", "*.xlsx *.xls"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo Excel",
            filetypes=filetypes
        )
        
        if filename:
            self.callback(filename)


class ResponsibleDialog:
    """Dialog for adding/editing responsible persons"""
    
    def __init__(self, parent, title, responsible=None):
        self.result = None
        self.responsible = responsible
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (250)
        y = (self.dialog.winfo_screenheight() // 2) - (200)
        self.dialog.geometry(f"500x400+{x}+{y}")
        
        self.setup_ui()
        
        # Load existing data if editing
        if self.responsible:
            self.load_responsible_data()
            
    def setup_ui(self):
        """Setup dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Form fields
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill="x", pady=(0, 20))
        
        # Name
        ttk.Label(fields_frame, text="Nome Completo *:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(fields_frame, textvariable=self.name_var, width=50)
        name_entry.grid(row=0, column=1, sticky="ew", pady=(0, 5))
        
        # CPF
        ttk.Label(fields_frame, text="CPF *:").grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.cpf_var = tk.StringVar()
        cpf_entry = ttk.Entry(fields_frame, textvariable=self.cpf_var, width=50)
        cpf_entry.grid(row=1, column=1, sticky="ew", pady=(0, 5))
        
        # NIP
        ttk.Label(fields_frame, text="NIP *:").grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.nip_var = tk.StringVar()
        nip_entry = ttk.Entry(fields_frame, textvariable=self.nip_var, width=50)
        nip_entry.grid(row=2, column=1, sticky="ew", pady=(0, 5))
        
        # Profile
        ttk.Label(fields_frame, text="Perfil *:").grid(row=3, column=0, sticky="w", pady=(0, 5))
        self.profile_var = tk.StringVar()
        profile_combo = ttk.Combobox(fields_frame, textvariable=self.profile_var, 
                                   values=PROFILES, state="readonly", width=47)
        profile_combo.grid(row=3, column=1, sticky="ew", pady=(0, 5))
        
        # Profile Type
        ttk.Label(fields_frame, text="Tipo Perfil OM *:").grid(row=4, column=0, sticky="w", pady=(0, 5))
        self.profile_type_var = tk.StringVar()
        profile_type_combo = ttk.Combobox(fields_frame, textvariable=self.profile_type_var, 
                                        values=PROFILE_TYPES, state="readonly", width=47)
        profile_type_combo.grid(row=4, column=1, sticky="ew", pady=(0, 5))
        
        # Code Papem
        ttk.Label(fields_frame, text="Código Papem:").grid(row=5, column=0, sticky="w", pady=(0, 5))
        self.code_papem_var = tk.StringVar(value="094")
        code_papem_entry = ttk.Entry(fields_frame, textvariable=self.code_papem_var, width=50)
        code_papem_entry.grid(row=5, column=1, sticky="ew", pady=(0, 5))
        
        # Configure grid weights
        fields_frame.columnconfigure(1, weight=1)
        
        # Validation info
        info_frame = ttk.LabelFrame(main_frame, text="Informações", padding="10")
        info_frame.pack(fill="x", pady=(0, 20))
        
        info_text = """• Campos marcados com * são obrigatórios
• CPF deve conter 11 dígitos (apenas números)
• Nome será convertido para maiúsculas
• Código Papem padrão: 094"""
        
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.cancel).pack(side="right", padx=(10, 0))
        ttk.Button(button_frame, text="Salvar", 
                  command=self.save).pack(side="right")
        
        # Add validation to CPF field
        vcmd = (self.dialog.register(self.validate_cpf_input), '%P')
        cpf_entry.config(validate='key', validatecommand=vcmd)
        
        # Focus on name field
        name_entry.focus()
        
    def validate_cpf_input(self, value):
        """Validate CPF input (only digits, max 11)"""
        if len(value) > 11:
            return False
        return value.isdigit() or value == ""
        
    def load_responsible_data(self):
        """Load existing responsible data"""
        self.name_var.set(self.responsible.nome)
        self.cpf_var.set(self.responsible.cpf)
        self.nip_var.set(self.responsible.nip)
        self.profile_var.set(self.responsible.perfil)
        self.profile_type_var.set(self.responsible.tipo_perfil_om)
        self.code_papem_var.set(self.responsible.cod_papem)
        
    def validate_form(self):
        """Validate form inputs"""
        # Check required fields
        if not self.name_var.get().strip():
            messagebox.showerror("Erro", "Nome é obrigatório")
            return False
            
        if not self.cpf_var.get().strip():
            messagebox.showerror("Erro", "CPF é obrigatório")
            return False
            
        if not self.nip_var.get().strip():
            messagebox.showerror("Erro", "NIP é obrigatório")
            return False
            
        if not self.profile_var.get():
            messagebox.showerror("Erro", "Perfil é obrigatório")
            return False
            
        if not self.profile_type_var.get():
            messagebox.showerror("Erro", "Tipo Perfil OM é obrigatório")
            return False
            
        # Validate CPF
        cpf = self.cpf_var.get().strip()
        if len(cpf) != 11:
            messagebox.showerror("Erro", "CPF deve conter 11 dígitos")
            return False
            
        if not validate_cpf(cpf):
            messagebox.showerror("Erro", "CPF inválido")
            return False
            
        return True
        
    def save(self):
        """Save responsible"""
        if not self.validate_form():
            return
            
        # Create responsible object
        self.result = Responsible(
            id=self.responsible.id if self.responsible else None,
            nome=self.name_var.get().strip().upper(),
            cpf=self.cpf_var.get().strip(),
            nip=self.nip_var.get().strip(),
            perfil=self.profile_var.get(),
            tipo_perfil_om=self.profile_type_var.get(),
            cod_papem=self.code_papem_var.get().strip() or "094"
        )
        
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()
