# Como Compilar o ExcelXml

## Opção 1: Usando os Scripts (Mais Fácil)

### Linux/macOS
```bash
# Compilar para todas as plataformas
./build.sh

# Compilar apenas para Windows
./build.sh windows

# Compilar apenas para Linux
./build.sh linux

# Compilar apenas para macOS
./build.sh macos
```

### Windows (PowerShell)
```powershell
# Compilar para todas as plataformas
.\build.ps1

# Compilar apenas para Windows
.\build.ps1 -Platform windows

# Compilar apenas para Linux
.\build.ps1 -Platform linux

# Compilar apenas para macOS
.\build.ps1 -Platform macos
```

## Opção 2: Manual (dotnet publish)

### Windows
```bash
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release -r win-x64 --self-contained true \
  -p:PublishSingleFile=true -o ./dist/windows
```

### Linux
```bash
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release -r linux-x64 --self-contained true \
  -p:PublishSingleFile=true -o ./dist/linux
```

### macOS
```bash
dotnet publish src/ExcelXml.Desktop/ExcelXml.Desktop.csproj \
  -c Release -r osx-arm64 --self-contained true \
  -p:PublishSingleFile=true -o ./dist/macos
```

## Criando Pacotes

### Pacote .deb (Linux/Debian)
```bash
# 1. Compilar para Linux
./build.sh linux

# 2. Criar pacote .deb
./create-deb.sh

# 3. Instalar
sudo dpkg -i excelxml_1.0.0_amd64.deb
```

### Bundle .app (macOS)
```bash
# 1. Compilar para macOS
./build.sh macos

# 2. Criar bundle (ARM64 para Apple Silicon)
./create-app-bundle.sh arm64

# 2. OU criar bundle (x64 para Intel)
./create-app-bundle.sh x64

# 3. Criar DMG (opcional)
hdiutil create -volname ExcelXml -srcfolder ExcelXml.app -ov -format UDZO ExcelXml.dmg
```

## Arquivos Gerados

Após a compilação, os executáveis estarão em:

- **Windows**: `dist/windows-x64/ExcelXml.Desktop.exe`
- **Linux**: `dist/linux-x64/ExcelXml.Desktop`
- **macOS ARM64**: `dist/macos-arm64/ExcelXml.Desktop`
- **macOS x64**: `dist/macos-x64/ExcelXml.Desktop`

## Tamanho dos Executáveis

Aproximadamente:
- Windows: ~65-80 MB (single-file, self-contained)
- Linux: ~65-80 MB (single-file, self-contained)
- macOS: ~70-85 MB (single-file, self-contained)

## Mais Informações

Veja o arquivo `GUIA_COMPILACAO.md` para detalhes completos sobre:
- Otimizações de build
- Diferentes configurações
- Troubleshooting
- Compilação cruzada (cross-platform)
