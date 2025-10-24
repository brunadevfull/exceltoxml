#!/bin/bash

# Script para criar pacote .deb para Linux
# Uso: ./create-deb.sh

set -e

APP_NAME="excelxml"
VERSION="1.0.0"
ARCH="amd64"
PACKAGE_NAME="${APP_NAME}_${VERSION}_${ARCH}"
BUILD_DIR="publish/linux-x64"
PACKAGE_DIR="$PACKAGE_NAME"

echo "=========================================="
echo "Criando pacote .deb para ExcelXml"
echo "=========================================="

# Verificar se o executável foi compilado
if [ ! -f "$BUILD_DIR/ExcelXml.Desktop" ]; then
    echo "Erro: Executável não encontrado em $BUILD_DIR"
    echo "Execute primeiro: dotnet publish -r linux-x64"
    exit 1
fi

# Limpar diretório anterior se existir
rm -rf "$PACKAGE_DIR"
rm -f "${PACKAGE_NAME}.deb"

# Criar estrutura de diretórios
echo "Criando estrutura de diretórios..."
mkdir -p "$PACKAGE_DIR/DEBIAN"
mkdir -p "$PACKAGE_DIR/usr/local/bin"
mkdir -p "$PACKAGE_DIR/usr/share/applications"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$PACKAGE_DIR/usr/share/doc/$APP_NAME"

# Copiar executável
echo "Copiando executável..."
cp "$BUILD_DIR/ExcelXml.Desktop" "$PACKAGE_DIR/usr/local/bin/$APP_NAME"
chmod +x "$PACKAGE_DIR/usr/local/bin/$APP_NAME"

# Criar arquivo de controle
echo "Criando arquivo de controle..."
cat > "$PACKAGE_DIR/DEBIAN/control" << EOF
Package: $APP_NAME
Version: $VERSION
Architecture: $ARCH
Maintainer: ExcelXml Team <contact@excelxml.com>
Description: ExcelXml - Conversor de Excel para XML
 Aplicação desktop para conversão de arquivos Excel para formato XML.
 Utiliza a interface Avalonia UI para uma experiência multiplataforma.
Section: office
Priority: optional
Depends: libicu72 | libicu70 | libicu69 | libicu68
EOF

# Criar arquivo .desktop
echo "Criando arquivo .desktop..."
cat > "$PACKAGE_DIR/usr/share/applications/$APP_NAME.desktop" << EOF
[Desktop Entry]
Type=Application
Name=ExcelXml
Comment=Conversor de Excel para XML
Exec=/usr/local/bin/$APP_NAME
Icon=$APP_NAME
Terminal=false
Categories=Office;Utility;
StartupNotify=true
EOF

# Criar arquivo copyright
cat > "$PACKAGE_DIR/usr/share/doc/$APP_NAME/copyright" << EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: ExcelXml
Source: https://github.com/brunadevfull/exceltoxml

Files: *
Copyright: 2025 ExcelXml Team
License: MIT
EOF

# Criar changelog
cat > "$PACKAGE_DIR/usr/share/doc/$APP_NAME/changelog.gz" << EOF
$APP_NAME ($VERSION) stable; urgency=low

  * Initial release

 -- ExcelXml Team <contact@excelxml.com>  $(date -R)
EOF
gzip -9 "$PACKAGE_DIR/usr/share/doc/$APP_NAME/changelog.gz" 2>/dev/null || true

# Criar script post-install (opcional)
cat > "$PACKAGE_DIR/DEBIAN/postinst" << EOF
#!/bin/bash
set -e

# Atualizar cache de aplicações
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q
fi

# Atualizar cache de ícones
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor || true
fi

exit 0
EOF
chmod +x "$PACKAGE_DIR/DEBIAN/postinst"

# Criar script pre-remove (opcional)
cat > "$PACKAGE_DIR/DEBIAN/prerm" << EOF
#!/bin/bash
set -e
exit 0
EOF
chmod +x "$PACKAGE_DIR/DEBIAN/prerm"

# Ajustar permissões
echo "Ajustando permissões..."
find "$PACKAGE_DIR" -type d -exec chmod 755 {} \;
find "$PACKAGE_DIR" -type f -exec chmod 644 {} \;
chmod +x "$PACKAGE_DIR/usr/local/bin/$APP_NAME"
chmod +x "$PACKAGE_DIR/DEBIAN/postinst"
chmod +x "$PACKAGE_DIR/DEBIAN/prerm"

# Construir pacote
echo "Construindo pacote .deb..."
dpkg-deb --build "$PACKAGE_DIR"

# Verificar pacote
echo "Verificando pacote..."
dpkg-deb --info "${PACKAGE_NAME}.deb"
echo ""
dpkg-deb --contents "${PACKAGE_NAME}.deb"

# Limpar diretório temporário
rm -rf "$PACKAGE_DIR"

echo ""
echo "=========================================="
echo "✓ Pacote criado com sucesso!"
echo "Arquivo: ${PACKAGE_NAME}.deb"
echo ""
echo "Para instalar:"
echo "  sudo dpkg -i ${PACKAGE_NAME}.deb"
echo ""
echo "Para desinstalar:"
echo "  sudo dpkg -r $APP_NAME"
echo "=========================================="
