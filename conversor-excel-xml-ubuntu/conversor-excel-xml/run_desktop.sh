#!/bin/bash

# Script para executar a aplicação desktop
# Conversor Excel → XML - Sistema Banco do Brasil

echo "🚀 Iniciando Conversor Excel → XML (Desktop)"
echo "============================================"

# Verificar se estamos no diretório correto
if [ ! -f "desktop_app.py" ]; then
    echo "❌ Arquivo desktop_app.py não encontrado!"
    echo "📁 Execute este script no diretório do projeto."
    exit 1
fi

# Verificar se ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "🔧 Execute primeiro: ./install_ubuntu.sh"
    exit 1
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar dependências
echo "🔍 Verificando dependências..."
python -c "import pandas, openpyxl, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependências faltando! Instalando..."
    pip install pandas openpyxl
fi

# Executar aplicação
echo "✅ Iniciando aplicação..."
python desktop_app.py

echo "👋 Aplicação encerrada."