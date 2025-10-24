#!/bin/bash

# Script para criar .app bundle para macOS
# Uso: ./create-app-bundle.sh [arm64|x64]

set -e

ARCH="${1:-arm64}"

if [ "$ARCH" != "arm64" ] && [ "$ARCH" != "x64" ]; then
    echo "Uso: $0 [arm64|x64]"
    exit 1
fi

APP_NAME="ExcelXml"
BUNDLE_NAME="${APP_NAME}.app"
BUILD_DIR="publish/osx-${ARCH}"
VERSION="1.0.0"

echo "=========================================="
echo "Criando .app bundle para macOS ($ARCH)"
echo "=========================================="

# Verificar se o executável foi compilado
if [ ! -f "$BUILD_DIR/ExcelXml.Desktop" ]; then
    echo "Erro: Executável não encontrado em $BUILD_DIR"
    echo "Execute primeiro: dotnet publish -r osx-$ARCH"
    exit 1
fi

# Limpar bundle anterior se existir
rm -rf "$BUNDLE_NAME"

# Criar estrutura do .app
echo "Criando estrutura do bundle..."
mkdir -p "$BUNDLE_NAME/Contents/MacOS"
mkdir -p "$BUNDLE_NAME/Contents/Resources"
mkdir -p "$BUNDLE_NAME/Contents/Frameworks"

# Copiar executável e dependências
echo "Copiando executável..."
cp "$BUILD_DIR/ExcelXml.Desktop" "$BUNDLE_NAME/Contents/MacOS/$APP_NAME"
chmod +x "$BUNDLE_NAME/Contents/MacOS/$APP_NAME"

# Copiar outras dependências se houver
if [ -d "$BUILD_DIR" ]; then
    echo "Copiando bibliotecas..."
    # Copiar dylibs se existirem
    find "$BUILD_DIR" -name "*.dylib" -exec cp {} "$BUNDLE_NAME/Contents/Frameworks/" \; 2>/dev/null || true
fi

# Criar Info.plist
echo "Criando Info.plist..."
cat > "$BUNDLE_NAME/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>$APP_NAME</string>
    <key>CFBundleIdentifier</key>
    <string>com.excelxml.desktop</string>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundleDisplayName</key>
    <string>$APP_NAME</string>
    <key>CFBundleVersion</key>
    <string>$VERSION</string>
    <key>CFBundleShortVersionString</key>
    <string>$VERSION</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.productivity</string>
</dict>
</plist>
EOF

# Criar PkgInfo
echo "APPL????" > "$BUNDLE_NAME/Contents/PkgInfo"

# Ajustar permissões
echo "Ajustando permissões..."
chmod -R 755 "$BUNDLE_NAME"
chmod +x "$BUNDLE_NAME/Contents/MacOS/$APP_NAME"

# Verificar estrutura
echo ""
echo "Estrutura do bundle:"
ls -R "$BUNDLE_NAME"

echo ""
echo "=========================================="
echo "✓ Bundle criado com sucesso!"
echo "Arquivo: $BUNDLE_NAME"
echo ""
echo "Para testar:"
echo "  open $BUNDLE_NAME"
echo ""
echo "Para criar DMG:"
echo "  hdiutil create -volname $APP_NAME -srcfolder $BUNDLE_NAME -ov -format UDZO ${APP_NAME}-${ARCH}.dmg"
echo "=========================================="
