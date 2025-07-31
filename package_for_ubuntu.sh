#!/bin/bash

# Script para empacotar aplicação para Ubuntu
# Conversor Excel → XML - Sistema Banco do Brasil

echo "📦 Empacotando aplicação para Ubuntu..."

# Nome do arquivo
PACKAGE_NAME="conversor-excel-xml-ubuntu.tar.gz"

# Criar diretório temporário
TEMP_DIR="conversor-excel-xml"
mkdir -p "$TEMP_DIR"

# Copiar arquivos necessários
echo "📄 Copiando arquivos..."

# Aplicação principal
cp desktop_app.py "$TEMP_DIR/"

# Código fonte
cp -r src/ "$TEMP_DIR/"

# Scripts de instalação
cp install_ubuntu.sh "$TEMP_DIR/"
cp create_desktop_shortcut.sh "$TEMP_DIR/"
cp run_desktop.sh "$TEMP_DIR/"

# Documentação
cp README_UBUNTU.md "$TEMP_DIR/"

# Tornar scripts executáveis
chmod +x "$TEMP_DIR"/*.sh

# Criar arquivo tar.gz
echo "🗜️ Compactando..."
tar -czf "$PACKAGE_NAME" "$TEMP_DIR"

# Limpar diretório temporário
rm -rf "$TEMP_DIR"

echo "✅ Pacote criado: $PACKAGE_NAME"
echo ""
echo "📋 INSTRUÇÕES PARA USAR NO UBUNTU:"
echo "1. Baixe o arquivo: $PACKAGE_NAME"
echo "2. Execute: tar -xzf $PACKAGE_NAME"
echo "3. Execute: cd conversor-excel-xml"
echo "4. Execute: ./install_ubuntu.sh"
echo "5. Execute: ./run_desktop.sh"
echo ""
echo "📖 Para mais detalhes, veja: README_UBUNTU.md"