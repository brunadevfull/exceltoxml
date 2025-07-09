"""
Responsible person model
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Responsible:
    """Model for responsible person"""
    nome: str
    cpf: str
    nip: str
    perfil: str
    tipo_perfil_om: str
    cod_papem: str = "094"
    id: Optional[int] = None
    ativo: bool = True
    data_cadastro: Optional[datetime] = None
    
    def __post_init__(self):
        """Post initialization processing"""
        if self.data_cadastro is None:
            self.data_cadastro = datetime.now()
            
        # Ensure nome is uppercase
        self.nome = self.nome.upper()
        
        # Ensure CPF is digits only
        self.cpf = ''.join(filter(str.isdigit, self.cpf))
        
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'nip': self.nip,
            'perfil': self.perfil,
            'tipo_perfil_om': self.tipo_perfil_om,
            'cod_papem': self.cod_papem,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        data_cadastro = None
        if data.get('data_cadastro'):
            data_cadastro = datetime.fromisoformat(data['data_cadastro'])
            
        return cls(
            id=data.get('id'),
            nome=data['nome'],
            cpf=data['cpf'],
            nip=data['nip'],
            perfil=data['perfil'],
            tipo_perfil_om=data['tipo_perfil_om'],
            cod_papem=data.get('cod_papem', '094'),
            ativo=data.get('ativo', True),
            data_cadastro=data_cadastro
        )
