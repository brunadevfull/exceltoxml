"""
Validation utilities
"""

import re
from typing import Optional

def validate_cpf(cpf: str) -> bool:
    """Validate CPF using Brazilian algorithm"""
    # Remove non-digits
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Check length
    if len(cpf) != 11:
        return False
        
    # Check for repeated digits
    if cpf == cpf[0] * 11:
        return False
        
    # Calculate first check digit
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    remainder1 = sum1 % 11
    digit1 = 0 if remainder1 < 2 else 11 - remainder1
    
    if int(cpf[9]) != digit1:
        return False
        
    # Calculate second check digit
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    remainder2 = sum2 % 11
    digit2 = 0 if remainder2 < 2 else 11 - remainder2
    
    return int(cpf[10]) == digit2

def validate_folha(folha: str) -> bool:
    """Validate folha format (MMAAAA)"""
    if not folha or len(folha) != 6:
        return False
        
    if not folha.isdigit():
        return False
        
    month = int(folha[:2])
    year = int(folha[2:])
    
    # Check valid month
    if month < 1 or month > 12:
        return False
        
    # Check reasonable year range
    if year < 2000 or year > 2100:
        return False
        
    return True

def validate_matricula(matricula: str) -> bool:
    """Validate matricula format"""
    if not matricula:
        return False
        
    # Should be digits only
    if not matricula.isdigit():
        return False
        
    # Should have reasonable length (typically 8 digits)
    if len(matricula) < 6 or len(matricula) > 10:
        return False
        
    return True

def validate_rubrica(rubrica: str) -> bool:
    """Validate rubrica format"""
    if not rubrica:
        return False
        
    # Should be exactly 7 digits
    if len(rubrica) != 7:
        return False
        
    if not rubrica.isdigit():
        return False
        
    return True

def validate_valor(valor: str) -> Optional[float]:
    """Validate and convert valor to float"""
    if not valor:
        return None
        
    # Replace comma with dot
    valor = valor.replace(',', '.')
    
    try:
        float_value = float(valor)
        if float_value < 0:
            return None
        return float_value
    except ValueError:
        return None

def validate_tipo(tipo: str) -> bool:
    """Validate tipo field"""
    if not tipo:
        return False
        
    return tipo.upper() in ['NO', 'DE']

def validate_trigrama(trigrama: str) -> bool:
    """Validate trigrama format"""
    if not trigrama:
        return False
        
    # Should be exactly 3 characters
    if len(trigrama) != 3:
        return False
        
    # Should be letters only
    if not trigrama.isalpha():
        return False
        
    return True

def format_cpf(cpf: str) -> str:
    """Format CPF for display"""
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

def clean_cpf(cpf: str) -> str:
    """Clean CPF keeping only digits"""
    return ''.join(filter(str.isdigit, cpf))
