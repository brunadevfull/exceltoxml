#!/bin/bash

# Script de instalação para Ubuntu
# Conversor Excel → XML - Sistema Banco do Brasil

echo "🚀 Instalação do Conversor Excel → XML para Ubuntu"
echo "=================================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instalando..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
else
    echo "✅ Python3 encontrado: $(python3 --version)"
fi

# Verificar se tkinter está disponível
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "❌ Tkinter não encontrado. Instalando..."
    sudo apt install -y python3-tk
else
    echo "✅ Tkinter disponível"
fi

# Criar diretório do projeto
PROJECT_DIR="$HOME/conversor-excel-xml"
echo "📁 Criando diretório do projeto: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install pandas openpyxl

# Criar estrutura de diretórios
echo "📂 Criando estrutura de diretórios..."
mkdir -p src/gui src/models src/services src/utils

echo "✅ Instalação base concluída!"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Copie todos os arquivos do projeto para: $PROJECT_DIR"
echo "2. Execute: cd $PROJECT_DIR && source venv/bin/activate"
echo "3. Execute: python desktop_app.py"
echo ""
echo "🔧 Para criar um atalho no desktop, execute:"
echo "   bash create_desktop_shortcut.sh"