# Script de compilação multi-plataforma para ExcelXml (PowerShell)
# Uso: .\build.ps1 [-Platform windows|linux|macos|all]

param(
    [Parameter()]
    [ValidateSet('windows', 'linux', 'macos', 'all')]
    [string]$Platform = 'all'
)

$ErrorActionPreference = "Stop"

$PROJECT = "src/ExcelXml.Desktop/ExcelXml.Desktop.csproj"
$OUTPUT_DIR = "dist"
$VERSION = "1.0.0"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "ExcelXml - Build Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

function Build-Windows {
    Write-Host "Compilando para Windows (x64)..." -ForegroundColor Yellow
    dotnet publish $PROJECT `
        -c Release `
        -r win-x64 `
        --self-contained true `
        -p:PublishSingleFile=true `
        -p:IncludeNativeLibrariesForSelfExtract=true `
        -p:PublishReadyToRun=true `
        -o "$OUTPUT_DIR/windows-x64"
    Write-Host "✓ Windows build completo: $OUTPUT_DIR/windows-x64/ExcelXml.Desktop.exe" -ForegroundColor Green
}

function Build-Linux {
    Write-Host "Compilando para Linux (x64)..." -ForegroundColor Yellow
    dotnet publish $PROJECT `
        -c Release `
        -r linux-x64 `
        --self-contained true `
        -p:PublishSingleFile=true `
        -p:IncludeNativeLibrariesForSelfExtract=true `
        -p:PublishReadyToRun=true `
        -o "$OUTPUT_DIR/linux-x64"
    Write-Host "✓ Linux build completo: $OUTPUT_DIR/linux-x64/ExcelXml.Desktop" -ForegroundColor Green
}

function Build-MacOS {
    Write-Host "Compilando para macOS (ARM64 - Apple Silicon)..." -ForegroundColor Yellow
    dotnet publish $PROJECT `
        -c Release `
        -r osx-arm64 `
        --self-contained true `
        -p:PublishSingleFile=true `
        -p:IncludeNativeLibrariesForSelfExtract=true `
        -o "$OUTPUT_DIR/macos-arm64"
    Write-Host "✓ macOS ARM64 build completo: $OUTPUT_DIR/macos-arm64/ExcelXml.Desktop" -ForegroundColor Green

    Write-Host "Compilando para macOS (x64 - Intel)..." -ForegroundColor Yellow
    dotnet publish $PROJECT `
        -c Release `
        -r osx-x64 `
        --self-contained true `
        -p:PublishSingleFile=true `
        -p:IncludeNativeLibrariesForSelfExtract=true `
        -o "$OUTPUT_DIR/macos-x64"
    Write-Host "✓ macOS x64 build completo: $OUTPUT_DIR/macos-x64/ExcelXml.Desktop" -ForegroundColor Green
}

function Build-All {
    Build-Windows
    Write-Host ""
    Build-Linux
    Write-Host ""
    Build-MacOS
}

# Criar diretório de saída
New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

# Processar plataforma
switch ($Platform) {
    'windows' { Build-Windows }
    'linux' { Build-Linux }
    'macos' { Build-MacOS }
    'all' { Build-All }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Build concluído com sucesso!" -ForegroundColor Green
Write-Host "Arquivos em: $OUTPUT_DIR/" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
