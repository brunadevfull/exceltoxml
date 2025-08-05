# Conversor Excel → XML - Instalação Ubuntu

## Requisitos do Sistema

- Ubuntu 18.04 ou superior
- Python 3.6 ou superior
- Tkinter (interface gráfica)
- Conexão com internet (apenas para instalação)

## Instalação Automática

### 1. Download dos Arquivos

Baixe todos os arquivos do projeto para uma pasta no seu computador.

### 2. Instalação

Abra o terminal na pasta do projeto e execute:

```bash
chmod +x install_ubuntu.sh
./install_ubuntu.sh
```

Este script irá:
- ✅ Instalar Python3 e Tkinter (se necessário)
- ✅ Criar ambiente virtual
- ✅ Instalar dependências (pandas, openpyxl)
- ✅ Configurar estrutura de diretórios

### 3. Copiar Arquivos do Projeto

Copie todos os arquivos para o diretório criado:

```bash
cp -r * ~/conversor-excel-xml/
```

### 4. Executar Aplicação

```bash
cd ~/conversor-excel-xml
source venv/bin/activate
python desktop_app.py
```

### 5. Criar Atalho no Desktop (Opcional)

```bash
chmod +x create_desktop_shortcut.sh
./create_desktop_shortcut.sh
```

## Instalação Manual

Se preferir instalar manualmente:

### 1. Instalar Dependências do Sistema

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk
```

### 2. Criar e Ativar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências Python

```bash
pip install pandas openpyxl
```

### 4. Executar Aplicação

```bash
python desktop_app.py
```

## Uso da Aplicação

### Interface Principal

A aplicação possui uma interface gráfica dividida em:

1. **Área de Upload**: Para selecionar arquivos Excel
2. **Configurações**: Responsável e parâmetros
3. **Status e Progresso**: Acompanhamento da conversão
4. **Gerenciamento**: Lista de responsáveis

### Passo a Passo

1. **Selecionar Arquivo Excel**
   - Clique em "Selecionar Arquivo"
   - Escolha um arquivo .xlsx ou .xls
   - O arquivo será validado automaticamente

2. **Configurar Responsável**
   - Selecione um responsável da lista
   - Para adicionar novo: clique em "Novo Responsável"

3. **Informar Folha**
   - Digite no formato MMAAAA
   - Exemplo: 012024 para Janeiro/2024

4. **Converter**
   - Clique em "Converter para XML"
   - Escolha onde salvar o arquivo XML

### Formato do Excel

O arquivo Excel deve conter as colunas:
- `matricula`: Matrícula do funcionário
- `rubrica`: Código da rubrica (7 dígitos)
- `valor`: Valor do comando
- `tipo`: NO (novo) ou DE (desconto)
- `trigrama`: Código de 3 letras

### Modelo Excel

Use o botão "Baixar Modelo Excel" para obter um exemplo.

## Solução de Problemas

### Erro: "No module named 'tkinter'"

```bash
sudo apt install python3-tk
```

### Erro: "No module named 'pandas'"

```bash
source venv/bin/activate
pip install pandas openpyxl
```

### Interface não aparece

Verifique se você está em um ambiente gráfico (não terminal remoto):

```bash
echo $DISPLAY
```

Se vazio, você precisa estar em uma sessão gráfica.

### Permissões negadas

```bash
chmod +x *.sh
```

## Estrutura de Arquivos

```
conversor-excel-xml/
├── desktop_app.py          # Aplicação principal
├── src/
│   ├── gui/
│   │   ├── main_window.py  # Interface principal
│   │   └── widgets.py      # Componentes personalizados
│   ├── models/
│   │   └── responsible.py  # Modelo de responsável
│   ├── services/
│   │   ├── data_manager.py    # Gerenciamento de dados
│   │   ├── excel_processor.py # Processamento Excel
│   │   └── xml_generator.py   # Geração XML
│   └── utils/
│       ├── constants.py    # Constantes
│       └── validators.py   # Validadores
├── venv/                   # Ambiente virtual
├── install_ubuntu.sh       # Script de instalação
└── README_UBUNTU.md        # Este arquivo
```

## Configurações

As configurações são salvas automaticamente em:
- `~/.config/conversorexcelxml/config.json`

## Backups

Backups automáticos são criados em:
- `~/.config/conversorexcelxml/backups/`

## Suporte

Para problemas ou dúvidas:
1. Verifique se todas as dependências estão instaladas
2. Confirme que está usando Python 3.6+
3. Teste com o arquivo modelo Excel fornecido
4. Verifique os logs de erro na interface da aplicação