#!/bin/bash

# Script de compilação multi-plataforma para ExcelXml
# Uso: ./build.sh [windows|linux|macos|all]

set -e

PROJECT="src/ExcelXml.Desktop/ExcelXml.Desktop.csproj"
OUTPUT_DIR="dist"
VERSION="1.0.0"

echo "=========================================="
echo "ExcelXml - Build Script"
echo "=========================================="

build_windows() {
    echo "Compilando para Windows (x64)..."
    dotnet publish "$PROJECT" \
        -c Release \
        -r win-x64 \
        --self-contained true \
        -p:PublishSingleFile=true \
        -p:IncludeNativeLibrariesForSelfExtract=true \
        -p:PublishReadyToRun=true \
        -o "$OUTPUT_DIR/windows-x64"
    echo "✓ Windows build completo: $OUTPUT_DIR/windows-x64/ExcelXml.Desktop.exe"
}

build_linux() {
    echo "Compilando para Linux (x64)..."
    dotnet publish "$PROJECT" \
        -c Release \
        -r linux-x64 \
        --self-contained true \
        -p:PublishSingleFile=true \
        -p:IncludeNativeLibrariesForSelfExtract=true \
        -p:PublishReadyToRun=true \
        -o "$OUTPUT_DIR/linux-x64"
    chmod +x "$OUTPUT_DIR/linux-x64/ExcelXml.Desktop"
    echo "✓ Linux build completo: $OUTPUT_DIR/linux-x64/ExcelXml.Desktop"
}

build_macos() {
    echo "Compilando para macOS (ARM64 - Apple Silicon)..."
    dotnet publish "$PROJECT" \
        -c Release \
        -r osx-arm64 \
        --self-contained true \
        -p:PublishSingleFile=true \
        -p:IncludeNativeLibrariesForSelfExtract=true \
        -o "$OUTPUT_DIR/macos-arm64"
    chmod +x "$OUTPUT_DIR/macos-arm64/ExcelXml.Desktop"
    echo "✓ macOS ARM64 build completo: $OUTPUT_DIR/macos-arm64/ExcelXml.Desktop"

    echo "Compilando para macOS (x64 - Intel)..."
    dotnet publish "$PROJECT" \
        -c Release \
        -r osx-x64 \
        --self-contained true \
        -p:PublishSingleFile=true \
        -p:IncludeNativeLibrariesForSelfExtract=true \
        -o "$OUTPUT_DIR/macos-x64"
    chmod +x "$OUTPUT_DIR/macos-x64/ExcelXml.Desktop"
    echo "✓ macOS x64 build completo: $OUTPUT_DIR/macos-x64/ExcelXml.Desktop"
}

build_all() {
    build_windows
    echo ""
    build_linux
    echo ""
    build_macos
}

# Criar diretório de saída
mkdir -p "$OUTPUT_DIR"

# Processar argumentos
case "${1:-all}" in
    windows)
        build_windows
        ;;
    linux)
        build_linux
        ;;
    macos)
        build_macos
        ;;
    all)
        build_all
        ;;
    *)
        echo "Uso: $0 [windows|linux|macos|all]"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Build concluído com sucesso!"
echo "Arquivos em: $OUTPUT_DIR/"
echo "=========================================="
