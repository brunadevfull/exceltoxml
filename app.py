#!/usr/bin/env python3
"""
Conversor Excel → XML - Sistema Banco do Brasil
Aplicação web para converter planilhas Excel em arquivos XML
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import os
import sys
from pathlib import Path
import traceback
import tempfile
from werkzeug.utils import secure_filename
import io

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.data_manager import DataManager
from services.excel_processor import ExcelProcessor
from services.xml_generator import XMLGenerator
from models.responsible import Responsible
from utils.validators import validate_cpf
from utils.constants import PROFILES, PROFILE_TYPES

app = Flask(__name__)
app.secret_key = 'excel_xml_converter_secret_key'

# Initialize services
data_manager = DataManager()
excel_processor = ExcelProcessor()
xml_generator = XMLGenerator()

# Configure upload folder
UPLOAD_FOLDER = tempfile.mkdtemp()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    responsibles = data_manager.get_responsibles()
    return render_template('index.html', 
                         responsibles=responsibles,
                         profiles=PROFILES,
                         profile_types=PROFILE_TYPES)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the Excel file
            data = excel_processor.process_file(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'records': len(data),
                'preview': data[:5] if data else []
            })
        
        return jsonify({'error': 'Formato de arquivo não suportado'}), 400
        
    except Exception as e:
        return jsonify({'error': f'Erro ao processar arquivo: {str(e)}'}), 500

@app.route('/convert', methods=['POST'])
def convert_file():
    """Convert Excel to XML"""
    try:
        data = request.json
        filename = data.get('filename')
        responsible_id = data.get('responsible_id')
        output_filename = data.get('output_filename', 'comandos_pagamento.xml')
        folha = data.get('folha')
        
        if not filename or not responsible_id or not folha:
            return jsonify({'error': 'Dados obrigatórios não fornecidos'}), 400
        
        # Get responsible
        responsible = data_manager.get_responsible_by_id(int(responsible_id))
        if not responsible:
            return jsonify({'error': 'Responsável não encontrado'}), 400
        
        # Process Excel file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Arquivo não encontrado'}), 400
        
        excel_data = excel_processor.process_file(filepath)
        
        # Generate XML
        xml_content = xml_generator.generate_xml(excel_data, responsible, folha)
        
        # Save XML to temporary file
        xml_filename = secure_filename(output_filename)
        if not xml_filename.endswith('.xml'):
            xml_filename += '.xml'
        
        xml_filepath = os.path.join(app.config['UPLOAD_FOLDER'], xml_filename)
        with open(xml_filepath, 'w', encoding='iso-8859-1') as f:
            f.write(xml_content)
        
        return jsonify({
            'success': True,
            'xml_filename': xml_filename,
            'records_processed': len(excel_data)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro na conversão: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated XML file"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'Arquivo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': f'Erro no download: {str(e)}'}), 500

@app.route('/responsibles', methods=['GET'])
def get_responsibles():
    """Get all responsibles"""
    responsibles = data_manager.get_responsibles()
    return jsonify([r.to_dict() for r in responsibles])

@app.route('/responsibles', methods=['POST'])
def add_responsible():
    """Add new responsible"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['nome', 'cpf', 'nip', 'perfil', 'tipo_perfil_om']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Validate CPF
        if not validate_cpf(data['cpf']):
            return jsonify({'error': 'CPF inválido'}), 400
        
        # Create responsible
        responsible = Responsible(
            nome=data['nome'].strip().upper(),
            cpf=data['cpf'].strip(),
            nip=data['nip'].strip(),
            perfil=data['perfil'],
            tipo_perfil_om=data['tipo_perfil_om'],
            cod_papem=data.get('cod_papem', '094')
        )
        
        # Save responsible
        data_manager.add_responsible(responsible)
        
        return jsonify({
            'success': True,
            'responsible': responsible.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao salvar responsável: {str(e)}'}), 500

@app.route('/template')
def download_template():
    """Download Excel template"""
    try:
        # Create a simple Excel template
        import pandas as pd
        
        template_data = {
            'MATRICULA': ['123456', '789012'],
            'NOME': ['JOÃO DA SILVA', 'MARIA SANTOS'],
            'CPF': ['12345678901', '98765432109'],
            'TRIGRAMA': ['ABC', 'DEF'],
            'RUBRICA': ['1234567', '7654321'],
            'VALOR': [1500.00, 2000.00]
        }
        
        df = pd.DataFrame(template_data)
        
        template_path = os.path.join(app.config['UPLOAD_FOLDER'], 'modelo_excel.xlsx')
        df.to_excel(template_path, index=False)
        
        return send_file(template_path, as_attachment=True, download_name='modelo_excel.xlsx')
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar modelo: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Excel to XML Converter Web App...")
    print("Access the application at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)