"""
Application constants
"""

# Available profiles
PROFILES = ["AGI", "ADM", "GER"]

# Available profile types
PROFILE_TYPES = ["IQM", "SUP", "ADM"]

# File extensions
EXCEL_EXTENSIONS = [".xlsx", ".xls"]
XML_EXTENSIONS = [".xml"]

# Validation constants
MIN_MATRICULA_LENGTH = 6
MAX_MATRICULA_LENGTH = 10
RUBRICA_LENGTH = 7
TRIGRAMA_LENGTH = 3
CPF_LENGTH = 11

# XML constants
XML_ENCODING = "iso-8859-1"
XML_STANDALONE = "yes"
XML_SISTEMA = "3"
XML_ALTERADOR = "I"
XML_FORM_PAGTO = "AV"

# Application info
APP_NAME = "Conversor Excel → XML"
APP_VERSION = "2.0"
APP_TITLE = f"{APP_NAME} - Sistema BB v{APP_VERSION}"

# Default values
DEFAULT_COD_PAPEM = "094"
DEFAULT_RESPONSIBLE_NAME = "RESPONSÁVEL PADRÃO"
DEFAULT_RESPONSIBLE_CPF = "00000000000"
DEFAULT_RESPONSIBLE_NIP = "00000"

# Error messages
ERROR_MESSAGES = {
    'file_not_found': "Arquivo não encontrado",
    'file_not_excel': "Arquivo deve ser do tipo Excel (.xlsx ou .xls)",
    'missing_columns': "Colunas obrigatórias ausentes",
    'invalid_cpf': "CPF inválido",
    'invalid_folha': "Folha deve estar no formato MMAAAA",
    'no_data': "Nenhum dado encontrado no arquivo",
    'invalid_data': "Dados inválidos encontrados",
    'save_error': "Erro ao salvar arquivo",
    'load_error': "Erro ao carregar arquivo"
}

# Success messages
SUCCESS_MESSAGES = {
    'file_processed': "Arquivo processado com sucesso",
    'xml_generated': "XML gerado com sucesso",
    'responsible_added': "Responsável adicionado com sucesso",
    'responsible_updated': "Responsável atualizado com sucesso",
    'responsible_removed': "Responsável removido com sucesso",
    'template_created': "Modelo Excel criado com sucesso"
}

# UI Constants
MAIN_WINDOW_SIZE = "1400x900"
MAIN_WINDOW_MIN_SIZE = "1200x700"
DIALOG_SIZE = "500x400"

# Colors
COLORS = {
    'success': '#28a745',
    'error': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8',
    'primary': '#007bff',
    'secondary': '#6c757d'
}

# Fonts
FONTS = {
    'title': ('Arial', 16, 'bold'),
    'subtitle': ('Arial', 10),
    'normal': ('Arial', 10),
    'small': ('Arial', 8)
}
