#!/bin/bash

# Script para criar atalho no desktop Ubuntu
# Conversor Excel → XML - Sistema Banco do Brasil

PROJECT_DIR="$HOME/conversor-excel-xml"
DESKTOP_FILE="$HOME/Desktop/conversor-excel-xml.desktop"

echo "🖥️ Criando atalho no desktop..."

# Criar arquivo .desktop
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Name=Conversor Excel → XML
Comment=Sistema de Comandos de Pagamento Banco do Brasil
Exec=bash -c "cd $PROJECT_DIR && source venv/bin/activate && python desktop_app.py"
Icon=$PROJECT_DIR/icon.png
Terminal=false
Type=Application
Categories=Office;Utility;
StartupNotify=true
EOF

# Tornar executável
chmod +x "$DESKTOP_FILE"

# Criar ícone simples (se não existir)
if [ ! -f "$PROJECT_DIR/icon.png" ]; then
    # Criar um ícone simples usando ImageMagick (se disponível)
    if command -v convert &> /dev/null; then
        convert -size 64x64 xc:blue -pointsize 20 -fill white -gravity center -annotate 0 "XML" "$PROJECT_DIR/icon.png"
        echo "✅ Ícone criado"
    else
        echo "⚠️ ImageMagick não encontrado. Ícone não criado."
    fi
fi

echo "✅ Atalho criado no desktop: $DESKTOP_FILE"
echo "🎯 Duplo clique no ícone 'Conversor Excel → XML' para executar"