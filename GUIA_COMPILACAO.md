# Guia de Compilação - ExcelXml

Este guia explica como compilar o ExcelXml.Desktop para diferentes plataformas.

## Pré-requisitos

- .NET 8.0 SDK instalado
- Projeto: `ExcelXml.Desktop` (aplicação Avalonia)

## Compilação Básica

### Desenvolvimento (Debug)
```bash
dotnet build
```

### Release
```bash
dotnet build -c Release
```

## Publicação para Distribuição

### 1. Windows (.exe)

#### Single-file executável (auto-contido)
```bash
# Windows x64
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release \
  -r win-x64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -p:IncludeNativeLibrariesForSelfExtract=true \
  -o ./publish/win-x64

# Windows ARM64
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release \
  -r win-arm64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -p:IncludeNativeLibrariesForSelfExtract=true \
  -o ./publish/win-arm64
```

**Resultado:** `ExcelXml.Desktop.exe` em `./publish/win-x64/`

#### Executável dependente do .NET Runtime
```bash
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release \
  -r win-x64 \
  --self-contained false \
  -o ./publish/win-x64-runtime-dependent
```

### 2. Linux (.deb package)

#### Passo 1: Publicar para Linux
```bash
# Linux x64
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release \
  -r linux-x64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -o ./publish/linux-x64

# Linux ARM64 (para Raspberry Pi, etc.)
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release \
  -r linux-arm64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -o ./publish/linux-arm64
```

#### Passo 2: Criar pacote .deb

Você pode usar `dotnet-packaging` ou criar manualmente:

**Opção A: Usando dotnet-packaging**
```bash
# Instalar ferramenta
dotnet tool install -g dotnet-deb

# Criar .deb
cd publish/linux-x64
dotnet deb install
```

**Opção B: Manual - Estrutura .deb**
```bash
# Criar estrutura de diretórios
mkdir -p excelxml_1.0.0_amd64/DEBIAN
mkdir -p excelxml_1.0.0_amd64/usr/local/bin
mkdir -p excelxml_1.0.0_amd64/usr/share/applications
mkdir -p excelxml_1.0.0_amd64/usr/share/icons/hicolor/256x256/apps

# Copiar executável
cp publish/linux-x64/ExcelXml.Desktop excelxml_1.0.0_amd64/usr/local/bin/excelxml

# Criar arquivo de controle
cat > excelxml_1.0.0_amd64/DEBIAN/control << EOF
Package: excelxml
Version: 1.0.0
Architecture: amd64
Maintainer: Seu Nome <email@exemplo.com>
Description: ExcelXml - Conversor de Excel para XML
 Aplicação desktop para conversão de arquivos Excel para XML.
Depends: libicu72 | libicu70 | libicu69
EOF

# Criar arquivo .desktop
cat > excelxml_1.0.0_amd64/usr/share/applications/excelxml.desktop << EOF
[Desktop Entry]
Type=Application
Name=ExcelXml
Comment=Conversor de Excel para XML
Exec=/usr/local/bin/excelxml
Icon=excelxml
Terminal=false
Categories=Office;Utility;
EOF

# Criar pacote
dpkg-deb --build excelxml_1.0.0_amd64
```

**Resultado:** `excelxml_1.0.0_amd64.deb`

**Instalar:**
```bash
sudo dpkg -i excelxml_1.0.0_amd64.deb
```

### 3. macOS (.app bundle)

#### Passo 1: Publicar para macOS
```bash
# macOS x64 (Intel)
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release \
  -r osx-x64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -o ./publish/osx-x64

# macOS ARM64 (Apple Silicon M1/M2/M3)
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release \
  -r osx-arm64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -o ./publish/osx-arm64
```

#### Passo 2: Criar .app bundle
```bash
# Criar estrutura do .app
mkdir -p ExcelXml.app/Contents/MacOS
mkdir -p ExcelXml.app/Contents/Resources

# Copiar executável
cp publish/osx-arm64/ExcelXml.Desktop ExcelXml.app/Contents/MacOS/ExcelXml
chmod +x ExcelXml.app/Contents/MacOS/ExcelXml

# Criar Info.plist
cat > ExcelXml.app/Contents/Info.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ExcelXml</string>
    <key>CFBundleIdentifier</key>
    <string>com.excelxml.desktop</string>
    <key>CFBundleName</key>
    <string>ExcelXml</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF
```

**Resultado:** `ExcelXml.app/`

**Criar DMG (opcional):**
```bash
# Em macOS
hdiutil create -volname ExcelXml -srcfolder ExcelXml.app -ov -format UDZO ExcelXml.dmg
```

## Runtime Identifiers (RIDs) Disponíveis

| Plataforma | RID | Descrição |
|------------|-----|-----------|
| Windows | `win-x64` | Windows 64-bit |
| Windows | `win-x86` | Windows 32-bit |
| Windows | `win-arm64` | Windows ARM64 |
| Linux | `linux-x64` | Linux 64-bit |
| Linux | `linux-arm` | Linux ARM32 |
| Linux | `linux-arm64` | Linux ARM64 |
| macOS | `osx-x64` | macOS Intel |
| macOS | `osx-arm64` | macOS Apple Silicon |

## Opções de Publicação

### Self-Contained vs Framework-Dependent

**Self-Contained (`--self-contained true`):**
- Inclui o .NET Runtime
- Maior tamanho (~60-100 MB)
- Funciona sem .NET instalado
- Recomendado para distribuição

**Framework-Dependent (`--self-contained false`):**
- Requer .NET 8.0 Runtime instalado
- Menor tamanho (~5-10 MB)
- Recomendado para ambientes controlados

### Single-File vs Multi-File

**Single-File (`-p:PublishSingleFile=true`):**
- Um único executável
- Mais fácil de distribuir
- Extração automática em temp

**Multi-File (padrão):**
- Executável + DLLs
- Inicialização ligeiramente mais rápida
- Mais difícil de distribuir

### Otimizações Adicionais

```bash
# Trimming (reduz tamanho removendo código não usado)
dotnet publish -c Release -r linux-x64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -p:PublishTrimmed=true \
  -p:TrimMode=link

# Ready to Run (R2R) - melhora startup
dotnet publish -c Release -r win-x64 \
  --self-contained true \
  -p:PublishSingleFile=true \
  -p:PublishReadyToRun=true
```

## Compilação Cruzada (Cross-Platform)

Você pode compilar para qualquer plataforma de qualquer OS:

```bash
# De Linux, compilar para Windows
dotnet publish -c Release -r win-x64 --self-contained true

# De Windows, compilar para Linux
dotnet publish -c Release -r linux-x64 --self-contained true

# De qualquer OS, compilar para macOS
dotnet publish -c Release -r osx-arm64 --self-contained true
```

## Testando a Compilação

```bash
# Após publicar, teste o executável
./publish/linux-x64/ExcelXml.Desktop        # Linux
./publish/osx-arm64/ExcelXml.Desktop        # macOS
./publish/win-x64/ExcelXml.Desktop.exe      # Windows
```

## Troubleshooting

### Erro: "The application to execute does not exist"
- Verifique se o caminho do projeto está correto
- Use caminho completo ou relativo correto para .csproj

### Executável não inicia
- Linux/macOS: Adicione permissão de execução `chmod +x <executável>`
- Verifique dependências do sistema (libicu, etc.)

### Tamanho muito grande
- Use `PublishTrimmed=true`
- Use `PublishReadyToRunUseCrossgen2=false`
- Considere framework-dependent ao invés de self-contained

### Avalonia não renderiza
- Certifique-se que as bibliotecas nativas estão incluídas
- Use `IncludeNativeLibrariesForSelfExtract=true`

## Scripts de Build Automatizados

Crie um script `build.sh` para automatizar:

```bash
#!/bin/bash

echo "Building ExcelXml for all platforms..."

# Windows
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release -r win-x64 --self-contained true \
  -p:PublishSingleFile=true -o ./dist/windows

# Linux
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release -r linux-x64 --self-contained true \
  -p:PublishSingleFile=true -o ./dist/linux

# macOS
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release -r osx-arm64 --self-contained true \
  -p:PublishSingleFile=true -o ./dist/macos

echo "Build complete! Check ./dist folder"
```

## Recursos Adicionais

- [.NET Publishing Guide](https://learn.microsoft.com/dotnet/core/deploying/)
- [Avalonia Deployment](https://docs.avaloniaui.net/docs/deployment/)
- [Runtime Identifiers](https://learn.microsoft.com/dotnet/core/rid-catalog)
