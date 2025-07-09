"""
Data manager for persistent storage
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import shutil

from models.responsible import Responsible

class DataManager:
    """Manage persistent data storage"""
    
    def __init__(self):
        self.config_dir = self._get_config_directory()
        self.config_file = self.config_dir / "config.json"
        self.backup_dir = self.config_dir / "backups"
        
        # Ensure directories exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create default config
        self.config = self._load_config()
        
    def _get_config_directory(self):
        """Get configuration directory based on OS"""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ['APPDATA']) / 'ConversorExcelXML'
        elif os.name == 'posix':  # Linux/macOS
            if 'darwin' in os.sys.platform:  # macOS
                config_dir = Path.home() / 'Library' / 'Application Support' / 'ConversorExcelXML'
            else:  # Linux
                config_dir = Path.home() / '.config' / 'conversorexcelxml'
        else:
            # Fallback to current directory
            config_dir = Path.cwd() / 'config'
            
        return config_dir
        
    def _load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
                
        # Create default config
        return self._create_default_config()
        
    def _create_default_config(self):
        """Create default configuration"""
        default_config = {
            "versao": "2.0",
            "ultimaAtualizacao": datetime.now().isoformat(),
            "responsaveis": [
                {
                    "id": 1,
                    "nome": "RESPONSÁVEL PADRÃO",
                    "cpf": "00000000000",
                    "nip": "00000",
                    "perfil": "AGI",
                    "tipo_perfil_om": "IQM",
                    "cod_papem": "094",
                    "ativo": True,
                    "data_cadastro": datetime.now().isoformat()
                }
            ]
        }
        
        self._save_config(default_config)
        return default_config
        
    def _save_config(self, config):
        """Save configuration to file"""
        try:
            # Create backup before saving
            self._create_backup()
            
            # Update timestamp
            config["ultimaAtualizacao"] = datetime.now().isoformat()
            
            # Save to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
            self.config = config
            
        except Exception as e:
            raise Exception(f"Erro ao salvar configuração: {e}")
            
    def _create_backup(self):
        """Create backup of current config"""
        if self.config_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"config_backup_{timestamp}.json"
            shutil.copy2(self.config_file, backup_file)
            
            # Keep only last 10 backups
            backups = sorted(self.backup_dir.glob("config_backup_*.json"))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
                    
    def get_responsibles(self) -> List[Responsible]:
        """Get all active responsibles"""
        responsibles = []
        for resp_data in self.config.get("responsaveis", []):
            if resp_data.get("ativo", True):
                responsibles.append(Responsible.from_dict(resp_data))
        return responsibles
        
    def add_responsible(self, responsible: Responsible):
        """Add new responsible"""
        # Check for duplicate CPF
        existing_responsibles = self.get_responsibles()
        if any(r.cpf == responsible.cpf for r in existing_responsibles):
            raise Exception("CPF já cadastrado")
            
        # Generate new ID
        max_id = max([r.get("id", 0) for r in self.config.get("responsaveis", [])], default=0)
        responsible.id = max_id + 1
        
        # Add to config
        self.config["responsaveis"].append(responsible.to_dict())
        self._save_config(self.config)
        
    def update_responsible(self, responsible_id: int, responsible: Responsible):
        """Update existing responsible"""
        # Find and update
        for i, resp_data in enumerate(self.config["responsaveis"]):
            if resp_data["id"] == responsible_id:
                responsible.id = responsible_id
                self.config["responsaveis"][i] = responsible.to_dict()
                self._save_config(self.config)
                return
                
        raise Exception("Responsável não encontrado")
        
    def remove_responsible(self, responsible_id: int):
        """Remove responsible (mark as inactive)"""
        for resp_data in self.config["responsaveis"]:
            if resp_data["id"] == responsible_id:
                resp_data["ativo"] = False
                self._save_config(self.config)
                return
                
        raise Exception("Responsável não encontrado")
        
    def get_responsible_by_id(self, responsible_id: int) -> Optional[Responsible]:
        """Get responsible by ID"""
        for resp_data in self.config.get("responsaveis", []):
            if resp_data["id"] == responsible_id and resp_data.get("ativo", True):
                return Responsible.from_dict(resp_data)
        return None
